# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2018 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

import heapq
from enum import Enum
from random import Random, getrandbits
from weakref import WeakKeyDictionary
from collections import defaultdict

import attr

from hypothesis import settings as Settings
from hypothesis import Phase, HealthCheck
from hypothesis.reporting import debug_report
from hypothesis.internal.compat import Counter, ceil, hbytes, hrange, \
    int_to_text, int_to_bytes, benchmark_time, int_from_bytes, \
    to_bytes_sequence, unicode_safe_repr
from hypothesis.utils.conventions import UniqueIdentifier
from hypothesis.internal.healthcheck import fail_health_check
from hypothesis.internal.conjecture.data import MAX_DEPTH, Status, \
    StopTest, ConjectureData
from hypothesis.internal.conjecture.minimizer import minimize

# Tell pytest to omit the body of this module from tracebacks
# http://doc.pytest.org/en/latest/example/simple.html#writing-well-integrated-assertion-helpers
__tracebackhide__ = True


HUNG_TEST_TIME_LIMIT = 5 * 60


@attr.s
class HealthCheckState(object):
    valid_examples = attr.ib(default=0)
    invalid_examples = attr.ib(default=0)
    overrun_examples = attr.ib(default=0)
    draw_times = attr.ib(default=attr.Factory(list))


class ExitReason(Enum):
    max_examples = 0
    max_iterations = 1
    timeout = 2
    max_shrinks = 3
    finished = 4
    flaky = 5


class RunIsComplete(Exception):
    pass


class ConjectureRunner(object):

    def __init__(
        self, test_function, settings=None, random=None,
        database_key=None,
    ):
        self._test_function = test_function
        self.settings = settings or Settings()
        self.shrinks = 0
        self.call_count = 0
        self.event_call_counts = Counter()
        self.valid_examples = 0
        self.start_time = benchmark_time()
        self.random = random or Random(getrandbits(128))
        self.database_key = database_key
        self.status_runtimes = {}

        self.all_drawtimes = []
        self.all_runtimes = []

        self.events_to_strings = WeakKeyDictionary()

        self.target_selector = TargetSelector(self.random)

        # Tree nodes are stored in an array to prevent heavy nesting of data
        # structures. Branches are dicts mapping bytes to child nodes (which
        # will in general only be partially populated). Leaves are
        # ConjectureData objects that have been previously seen as the result
        # of following that path.
        self.tree = [{}]

        # A node is dead if there is nothing left to explore past that point.
        # Recursively, a node is dead if either it is a leaf or every byte
        # leads to a dead node when starting from here.
        self.dead = set()

        # We rewrite the byte stream at various points during parsing, to one
        # that will produce an equivalent result but is in some sense more
        # canonical. We keep track of these so that when walking the tree we
        # can identify nodes where the exact byte value doesn't matter and
        # treat all bytes there as equivalent. This significantly reduces the
        # size of the search space and removes a lot of redundant examples.

        # Maps tree indices where to the unique byte that is valid at that
        # point. Corresponds to data.write() calls.
        self.forced = {}

        # Maps tree indices to the maximum byte that is valid at that point.
        # Currently this is only used inside draw_bits, but it potentially
        # could get used elsewhere.
        self.capped = {}

        # Where a tree node consists of the beginning of a block we track the
        # size of said block. This allows us to tell when an example is too
        # short even if it goes off the unexplored region of the tree - if it
        # is at the beginning of a block of size 4 but only has 3 bytes left,
        # it's going to overrun the end of the buffer regardless of the
        # buffer contents.
        self.block_sizes = {}

        self.interesting_examples = {}
        self.covering_examples = {}

        self.shrunk_examples = set()

        self.tag_intern_table = {}

        self.health_check_state = None

        self.used_examples_from_database = False

    def __tree_is_exhausted(self):
        return 0 in self.dead

    def test_function(self, data):
        if benchmark_time() - self.start_time >= HUNG_TEST_TIME_LIMIT:
            fail_health_check(self.settings, (
                'Your test has been running for at least five minutes. This '
                'is probably not what you intended, so by default Hypothesis '
                'turns it into an error.'
            ), HealthCheck.hung_test)

        self.call_count += 1
        try:
            self._test_function(data)
            data.freeze()
        except StopTest as e:
            if e.testcounter != data.testcounter:
                self.save_buffer(data.buffer)
                raise e
        except BaseException:
            self.save_buffer(data.buffer)
            raise
        finally:
            data.freeze()
            self.note_details(data)

        self.target_selector.add(data)

        self.debug_data(data)

        tags = frozenset(data.tags)
        data.tags = self.tag_intern_table.setdefault(tags, tags)

        if data.status == Status.VALID:
            self.valid_examples += 1
            for t in data.tags:
                existing = self.covering_examples.get(t)
                if (
                    existing is None or
                    sort_key(data.buffer) < sort_key(existing.buffer)
                ):
                    self.covering_examples[t] = data
                    if self.database is not None:
                        self.database.save(self.covering_key, data.buffer)
                        if existing is not None:
                            self.database.delete(
                                self.covering_key, existing.buffer)

        tree_node = self.tree[0]
        indices = []
        node_index = 0
        for i, b in enumerate(data.buffer):
            indices.append(node_index)
            if i in data.forced_indices:
                self.forced[node_index] = b
            try:
                self.capped[node_index] = data.capped_indices[i]
            except KeyError:
                pass
            try:
                node_index = tree_node[b]
            except KeyError:
                node_index = len(self.tree)
                self.tree.append({})
                tree_node[b] = node_index
            tree_node = self.tree[node_index]
            if node_index in self.dead:
                break

        for u, v in data.blocks:
            # This can happen if we hit a dead node when walking the buffer.
            # In that case we alrady have this section of the tree mapped.
            if u >= len(indices):
                break
            self.block_sizes[indices[u]] = v - u

        if data.status != Status.OVERRUN and node_index not in self.dead:
            self.dead.add(node_index)
            self.tree[node_index] = data

            for j in reversed(indices):
                if (
                    len(self.tree[j]) < self.capped.get(j, 255) + 1 and
                    j not in self.forced
                ):
                    break
                if set(self.tree[j].values()).issubset(self.dead):
                    self.dead.add(j)
                else:
                    break

        if data.status == Status.INTERESTING:
            key = data.interesting_origin
            changed = False
            try:
                existing = self.interesting_examples[key]
            except KeyError:
                changed = True
            else:
                if sort_key(data.buffer) < sort_key(existing.buffer):
                    self.shrinks += 1
                    self.downgrade_buffer(existing.buffer)
                    changed = True

            if changed:
                self.save_buffer(data.buffer)
                self.interesting_examples[key] = data
                self.shrunk_examples.discard(key)

            if self.shrinks >= self.settings.max_shrinks:
                self.exit_with(ExitReason.max_shrinks)
        if (
            self.settings.timeout > 0 and
            benchmark_time() >= self.start_time + self.settings.timeout
        ):
            self.exit_with(ExitReason.timeout)

        if not self.interesting_examples:
            if self.valid_examples >= self.settings.max_examples:
                self.exit_with(ExitReason.max_examples)
            if self.call_count >= max(
                self.settings.max_iterations, self.settings.max_examples
            ):
                self.exit_with(ExitReason.max_iterations)

        if self.__tree_is_exhausted():
            self.exit_with(ExitReason.finished)

        self.record_for_health_check(data)

    def record_for_health_check(self, data):
        # Once we've actually found a bug, there's no point in trying to run
        # health checks - they'll just mask the actually important information.
        if data.status == Status.INTERESTING:
            self.health_check_state = None

        state = self.health_check_state

        if state is None:
            return

        state.draw_times.extend(data.draw_times)

        if data.status == Status.VALID:
            state.valid_examples += 1
        elif data.status == Status.INVALID:
            state.invalid_examples += 1
        else:
            assert data.status == Status.OVERRUN
            state.overrun_examples += 1

        max_valid_draws = 10
        max_invalid_draws = 50
        max_overrun_draws = 20

        assert state.valid_examples <= max_valid_draws

        if state.valid_examples == max_valid_draws:
            self.health_check_state = None
            return

        if state.overrun_examples == max_overrun_draws:
            fail_health_check(self.settings, (
                'Examples routinely exceeded the max allowable size. '
                '(%d examples overran while generating %d valid ones)'
                '. Generating examples this large will usually lead to'
                ' bad results. You could try setting max_size parameters '
                'on your collections and turning '
                'max_leaves down on recursive() calls.') % (
                state.overrun_examples, state.valid_examples
            ), HealthCheck.data_too_large)
        if state.invalid_examples == max_invalid_draws:
            fail_health_check(self.settings, (
                'It looks like your strategy is filtering out a lot '
                'of data. Health check found %d filtered examples but '
                'only %d good ones. This will make your tests much '
                'slower, and also will probably distort the data '
                'generation quite a lot. You should adapt your '
                'strategy to filter less. This can also be caused by '
                'a low max_leaves parameter in recursive() calls') % (
                state.invalid_examples, state.valid_examples
            ), HealthCheck.filter_too_much)

        draw_time = sum(state.draw_times)

        if draw_time > 1.0:
            fail_health_check(self.settings, (
                'Data generation is extremely slow: Only produced '
                '%d valid examples in %.2f seconds (%d invalid ones '
                'and %d exceeded maximum size). Try decreasing '
                "size of the data you're generating (with e.g."
                'max_size or max_leaves parameters).'
            ) % (
                state.valid_examples, draw_time, state.invalid_examples,
                state.overrun_examples), HealthCheck.too_slow,)

    def save_buffer(self, buffer):
        if self.settings.database is not None:
            key = self.database_key
            if key is None:
                return
            self.settings.database.save(key, hbytes(buffer))

    def downgrade_buffer(self, buffer):
        if self.settings.database is not None:
            self.settings.database.move(
                self.database_key, self.secondary_key, buffer)

    @property
    def secondary_key(self):
        return b'.'.join((self.database_key, b'secondary'))

    @property
    def covering_key(self):
        return b'.'.join((self.database_key, b'coverage'))

    def note_details(self, data):
        runtime = max(data.finish_time - data.start_time, 0.0)
        self.all_runtimes.append(runtime)
        self.all_drawtimes.extend(data.draw_times)
        self.status_runtimes.setdefault(data.status, []).append(runtime)
        for event in set(map(self.event_to_string, data.events)):
            self.event_call_counts[event] += 1

    def debug(self, message):
        with self.settings:
            debug_report(message)

    def debug_data(self, data):
        buffer_parts = [u"["]
        for i, (u, v) in enumerate(data.blocks):
            if i > 0:
                buffer_parts.append(u" || ")
            buffer_parts.append(
                u', '.join(int_to_text(int(i)) for i in data.buffer[u:v]))
        buffer_parts.append(u']')

        status = unicode_safe_repr(data.status)

        if data.status == Status.INTERESTING:
            status = u'%s (%s)' % (
                status, unicode_safe_repr(data.interesting_origin,))

        self.debug(u'%d bytes %s -> %s, %s' % (
            data.index,
            u''.join(buffer_parts),
            status,
            data.output,
        ))

    def run(self):
        with self.settings:
            try:
                self._run()
            except RunIsComplete:
                pass
            for v in self.interesting_examples.values():
                self.debug_data(v)
            self.debug(
                u'Run complete after %d examples (%d valid) and %d shrinks' % (
                    self.call_count, self.valid_examples, self.shrinks,
                ))

    def _new_mutator(self):
        target_data = [None]

        def draw_new(data, n):
            return uniform(self.random, n)

        def draw_existing(data, n):
            return target_data[0].buffer[data.index:data.index + n]

        def draw_smaller(data, n):
            existing = target_data[0].buffer[data.index:data.index + n]
            r = uniform(self.random, n)
            if r <= existing:
                return r
            return _draw_predecessor(self.random, existing)

        def draw_larger(data, n):
            existing = target_data[0].buffer[data.index:data.index + n]
            r = uniform(self.random, n)
            if r >= existing:
                return r
            return _draw_successor(self.random, existing)

        def reuse_existing(data, n):
            choices = data.block_starts.get(n, []) or \
                target_data[0].block_starts.get(n, [])
            if choices:
                i = self.random.choice(choices)
                return target_data[0].buffer[i:i + n]
            else:
                result = uniform(self.random, n)
                assert isinstance(result, hbytes)
                return result

        def flip_bit(data, n):
            buf = bytearray(
                target_data[0].buffer[data.index:data.index + n])
            i = self.random.randint(0, n - 1)
            k = self.random.randint(0, 7)
            buf[i] ^= (1 << k)
            return hbytes(buf)

        def draw_zero(data, n):
            return hbytes(b'\0' * n)

        def draw_max(data, n):
            return hbytes([255]) * n

        def draw_constant(data, n):
            return hbytes([self.random.randint(0, 255)]) * n

        def redraw_last(data, n):
            u = target_data[0].blocks[-1][0]
            if data.index + n <= u:
                return target_data[0].buffer[data.index:data.index + n]
            else:
                return uniform(self.random, n)

        options = [
            draw_new,
            redraw_last, redraw_last,
            reuse_existing, reuse_existing,
            draw_existing, draw_smaller, draw_larger,
            flip_bit,
            draw_zero, draw_max, draw_zero, draw_max,
            draw_constant,
        ]

        bits = [
            self.random.choice(options) for _ in hrange(3)
        ]

        def mutate_from(origin):
            target_data[0] = origin
            return draw_mutated

        def draw_mutated(data, n):
            if data.index + n > len(target_data[0].buffer):
                result = uniform(self.random, n)
            else:
                result = self.random.choice(bits)(data, n)

            return self.__rewrite_for_novelty(
                data, self.__zero_bound(data, result))

        return mutate_from

    def __rewrite(self, data, result):
        return self.__rewrite_for_novelty(
            data, self.__zero_bound(data, result)
        )

    def __zero_bound(self, data, result):
        """This tries to get the size of the generated data under control by
        replacing the result with zero if we are too deep or have already
        generated too much data.

        This causes us to enter "shrinking mode" there and thus reduce
        the size of the generated data.

        """
        if (
            data.depth * 2 >= MAX_DEPTH or
            (data.index + len(result)) * 2 >= self.settings.buffer_size
        ):
            if any(result):
                data.hit_zero_bound = True
            return hbytes(len(result))
        else:
            return result

    def __rewrite_for_novelty(self, data, result):
        """Take a block that is about to be added to data as the result of a
        draw_bytes call and rewrite it a small amount to ensure that the result
        will be novel: that is, not hit a part of the tree that we have fully
        explored.

        This is mostly useful for test functions which draw a small
        number of blocks.

        """
        assert isinstance(result, hbytes)
        try:
            node_index = data.__current_node_index
        except AttributeError:
            node_index = 0
            data.__current_node_index = node_index
            data.__hit_novelty = False
            data.__evaluated_to = 0

        if data.__hit_novelty:
            return result

        node = self.tree[node_index]

        for i in hrange(data.__evaluated_to, len(data.buffer)):
            node = self.tree[node_index]
            try:
                node_index = node[data.buffer[i]]
                assert node_index not in self.dead
                node = self.tree[node_index]
            except KeyError:  # pragma: no cover
                assert False, (
                    'This should be impossible. If you see this error, please '
                    'report it as a bug (ideally with a reproducible test '
                    'case).'
                )

        for i, b in enumerate(result):
            assert isinstance(b, int)
            try:
                new_node_index = node[b]
            except KeyError:
                data.__hit_novelty = True
                return result

            new_node = self.tree[new_node_index]

            if new_node_index in self.dead:
                if isinstance(result, hbytes):
                    result = bytearray(result)
                for c in range(256):
                    if c not in node:
                        assert c <= self.capped.get(node_index, c)
                        result[i] = c
                        data.__hit_novelty = True
                        return hbytes(result)
                    else:
                        new_node_index = node[c]
                        new_node = self.tree[new_node_index]
                        if new_node_index not in self.dead:
                            result[i] = c
                            break
                else:  # pragma: no cover
                    assert False, (
                        'Found a tree node which is live despite all its '
                        'children being dead.')
            node_index = new_node_index
            node = new_node
        assert node_index not in self.dead
        data.__current_node_index = node_index
        data.__evaluated_to = data.index + len(result)
        return hbytes(result)

    @property
    def database(self):
        if self.database_key is None:
            return None
        return self.settings.database

    def has_existing_examples(self):
        return (
            self.database is not None and
            Phase.reuse in self.settings.phases
        )

    def reuse_existing_examples(self):
        """If appropriate (we have a database and have been told to use it),
        try to reload existing examples from the database.

        If there are a lot we don't try all of them. We always try the
        smallest example in the database (which is guaranteed to be the
        last failure) and the largest (which is usually the seed example
        which the last failure came from but we don't enforce that). We
        then take a random sampling of the remainder and try those. Any
        examples that are no longer interesting are cleared out.

        """
        if self.has_existing_examples():
            self.debug('Reusing examples from database')
            # We have to do some careful juggling here. We have two database
            # corpora: The primary and secondary. The primary corpus is a
            # small set of minimized examples each of which has at one point
            # demonstrated a distinct bug. We want to retry all of these.

            # We also have a secondary corpus of examples that have at some
            # point demonstrated interestingness (currently only ones that
            # were previously non-minimal examples of a bug, but this will
            # likely expand in future). These are a good source of potentially
            # interesting examples, but there are a lot of them, so we down
            # sample the secondary corpus to a more manageable size.

            corpus = sorted(
                self.settings.database.fetch(self.database_key),
                key=sort_key
            )
            desired_size = max(2, ceil(0.1 * self.settings.max_examples))

            for extra_key in [self.secondary_key, self.covering_key]:
                if len(corpus) < desired_size:
                    extra_corpus = list(
                        self.settings.database.fetch(extra_key),
                    )

                    shortfall = desired_size - len(corpus)

                    if len(extra_corpus) <= shortfall:
                        extra = extra_corpus
                    else:
                        extra = self.random.sample(extra_corpus, shortfall)
                    extra.sort(key=sort_key)
                    corpus.extend(extra)

            self.used_examples_from_database = len(corpus) > 0

            for existing in corpus:
                last_data = ConjectureData.for_buffer(existing)
                try:
                    self.test_function(last_data)
                finally:
                    if last_data.status != Status.INTERESTING:
                        self.settings.database.delete(
                            self.database_key, existing)
                        self.settings.database.delete(
                            self.secondary_key, existing)

    def exit_with(self, reason):
        self.exit_reason = reason
        raise RunIsComplete()

    def generate_new_examples(self):
        if Phase.generate not in self.settings.phases:
            return

        zero_data = self.cached_test_function(
            hbytes(self.settings.buffer_size))
        if zero_data.status == Status.OVERRUN or (
            zero_data.status == Status.VALID and
            len(zero_data.buffer) * 2 > self.settings.buffer_size
        ):
            fail_health_check(
                self.settings,
                'The smallest natural example for your test is extremely '
                'large. This makes it difficult for Hypothesis to generate '
                'good examples, especially when trying to reduce failing ones '
                'at the end. Consider reducing the size of your data if it is '
                'of a fixed size. You could also fix this by improving how '
                'your data shrinks (see https://hypothesis.readthedocs.io/en/'
                'latest/data.html#shrinking for details), or by introducing '
                'default values inside your strategy. e.g. could you replace '
                'some arguments with their defaults by using '
                'one_of(none(), some_complex_strategy)?',
                HealthCheck.large_base_example
            )

        if self.settings.perform_health_check:
            self.health_check_state = HealthCheckState()

        count = 0
        while not self.interesting_examples and (
            count < 10 or self.health_check_state is not None
        ):
            def draw_bytes(data, n):
                return self.__rewrite_for_novelty(
                    data, self.__zero_bound(data, uniform(self.random, n))
                )

            targets_found = len(self.covering_examples)

            last_data = ConjectureData(
                max_length=self.settings.buffer_size,
                draw_bytes=draw_bytes
            )
            self.test_function(last_data)
            last_data.freeze()

            if len(self.covering_examples) > targets_found:
                count = 0
            else:
                count += 1

        mutations = 0
        mutator = self._new_mutator()

        zero_bound_queue = []

        while not self.interesting_examples:
            if zero_bound_queue:
                # Whenever we generated an example and it hits a bound
                # which forces zero blocks into it, this creates a weird
                # distortion effect by making certain parts of the data
                # stream (especially ones to the right) much more likely
                # to be zero. We fix this by redistributing the generated
                # data by shuffling it randomly. This results in the
                # zero data being spread evenly throughout the buffer.
                # Hopefully the shrinking this causes will cause us to
                # naturally fail to hit the bound.
                # If it doesn't then we will queue the new version up again
                # (now with more zeros) and try again.
                overdrawn = zero_bound_queue.pop()
                buffer = bytearray(overdrawn.buffer)

                # These will have values written to them that are different
                # from what's in them anyway, so the value there doesn't
                # really "count" for distributional purposes, and if we
                # leave them in then they can cause the fraction of non
                # zero bytes to increase on redraw instead of decrease.
                for i in overdrawn.forced_indices:
                    buffer[i] = 0

                self.random.shuffle(buffer)
                buffer = hbytes(buffer)

                def draw_bytes(data, n):
                    result = buffer[data.index:data.index + n]
                    if len(result) < n:
                        result += hbytes(n - len(result))
                    return self.__rewrite(data, result)

                data = ConjectureData(
                    draw_bytes=draw_bytes,
                    max_length=self.settings.buffer_size,
                )
                self.test_function(data)
                data.freeze()
            else:
                target, origin = self.target_selector.select()
                mutations += 1
                targets_found = len(self.covering_examples)
                data = ConjectureData(
                    draw_bytes=mutator(origin),
                    max_length=self.settings.buffer_size
                )
                self.test_function(data)
                data.freeze()
                if (
                    data.status > origin.status or
                    len(self.covering_examples) > targets_found
                ):
                    mutations = 0
                elif (
                    data.status < origin.status or
                    not self.target_selector.has_tag(target, data) or
                    mutations >= 10
                ):
                    # Cap the variations of a single example and move on to
                    # an entirely fresh start.  Ten is an entirely arbitrary
                    # constant, but it's been working well for years.
                    mutations = 0
                    mutator = self._new_mutator()
            if getattr(data, 'hit_zero_bound', False):
                zero_bound_queue.append(data)
            mutations += 1

    def _run(self):
        self.start_time = benchmark_time()

        self.reuse_existing_examples()
        self.generate_new_examples()
        self.shrink_interesting_examples()

        self.exit_with(ExitReason.finished)

    def shrink_interesting_examples(self):
        """If we've found interesting examples, try to replace each of them
        with a minimal interesting example with the same interesting_origin.

        We may find one or more examples with a new interesting_origin
        during the shrink process. If so we shrink these too.

        """
        if (
            Phase.shrink not in self.settings.phases or
            not self.interesting_examples
        ):
            return

        for prev_data in sorted(
            self.interesting_examples.values(),
            key=lambda d: sort_key(d.buffer)
        ):
            assert prev_data.status == Status.INTERESTING
            data = ConjectureData.for_buffer(prev_data.buffer)
            self.test_function(data)
            if data.status != Status.INTERESTING:
                self.exit_with(ExitReason.flaky)

        self.clear_secondary_key()

        while len(self.shrunk_examples) < len(self.interesting_examples):
            target, example = min([
                (k, v) for k, v in self.interesting_examples.items()
                if k not in self.shrunk_examples],
                key=lambda kv: (sort_key(kv[1].buffer), sort_key(repr(kv[0]))),
            )
            self.debug('Shrinking %r' % (target,))

            def predicate(d):
                if d.status < Status.INTERESTING:
                    return False
                return d.interesting_origin == target

            self.shrink(example, predicate)

            self.shrunk_examples.add(target)

    def clear_secondary_key(self):
        if self.has_existing_examples():
            # If we have any smaller examples in the secondary corpus, now is
            # a good time to try them to see if they work as shrinks. They
            # probably won't, but it's worth a shot and gives us a good
            # opportunity to clear out the database.

            # It's not worth trying the primary corpus because we already
            # tried all of those in the initial phase.
            corpus = sorted(
                self.settings.database.fetch(self.secondary_key),
                key=sort_key
            )
            cap = max(
                sort_key(v.buffer)
                for v in self.interesting_examples.values()
            )
            for c in corpus:
                if sort_key(c) >= cap:
                    break
                else:
                    data = self.cached_test_function(c)
                    if (
                        data.status != Status.INTERESTING or
                        self.interesting_examples[data.interesting_origin]
                        is not data
                    ):
                        self.settings.database.delete(
                            self.secondary_key, c)

    def shrink(self, example, predicate):
        s = self.new_shrinker(example, predicate)
        s.shrink()
        return s.shrink_target

    def new_shrinker(self, example, predicate):
        return Shrinker(self, example, predicate)

    def prescreen_buffer(self, buffer):
        """Attempt to rule out buffer as a possible interesting candidate.

        Returns False if we know for sure that running this buffer will not
        produce an interesting result. Returns True if it might (because it
        explores territory we have not previously tried).

        This is purely an optimisation to try to reduce the number of tests we
        run. "return True" would be a valid but inefficient implementation.

        """
        node_index = 0
        n = len(buffer)
        for k, b in enumerate(buffer):
            if node_index in self.dead:
                return False
            try:
                # The block size at that point provides a lower bound on how
                # many more bytes are required. If the buffer does not have
                # enough bytes to fulfill that block size then we can rule out
                # this buffer.
                if k + self.block_sizes[node_index] > n:
                    return False
            except KeyError:
                pass
            try:
                b = self.forced[node_index]
            except KeyError:
                pass
            try:
                b = min(b, self.capped[node_index])
            except KeyError:
                pass
            try:
                node_index = self.tree[node_index][b]
            except KeyError:
                return True
        else:
            return False

    def cached_test_function(self, buffer):
        node_index = 0
        for i in hrange(self.settings.buffer_size):
            try:
                c = self.forced[node_index]
            except KeyError:
                if i < len(buffer):
                    c = buffer[i]
                else:
                    c = 0
            try:
                node_index = self.tree[node_index][c]
            except KeyError:
                break
            node = self.tree[node_index]
            if isinstance(node, ConjectureData):
                return node
        result = ConjectureData.for_buffer(buffer)
        self.test_function(result)
        return result

    def event_to_string(self, event):
        if isinstance(event, str):
            return event
        try:
            return self.events_to_strings[event]
        except KeyError:
            pass
        result = str(event)
        self.events_to_strings[event] = result
        return result


def _draw_predecessor(rnd, xs):
    r = bytearray()
    any_strict = False
    for x in to_bytes_sequence(xs):
        if not any_strict:
            c = rnd.randint(0, x)
            if c < x:
                any_strict = True
        else:
            c = rnd.randint(0, 255)
        r.append(c)
    return hbytes(r)


def _draw_successor(rnd, xs):
    r = bytearray()
    any_strict = False
    for x in to_bytes_sequence(xs):
        if not any_strict:
            c = rnd.randint(x, 255)
            if c > x:
                any_strict = True
        else:
            c = rnd.randint(0, 255)
        r.append(c)
    return hbytes(r)


def sort_key(buffer):
    return (len(buffer), buffer)


def uniform(random, n):
    return int_to_bytes(random.getrandbits(n * 8), n)


class SampleSet(object):
    """Set data type with the ability to sample uniformly at random from it.

    The mechanism is that we store the set in two parts: A mapping of
    values to their index in an array. Sampling uniformly at random then
    becomes simply a matter of sampling from the array, but we can use
    the index for efficient lookup to add and remove values.

    """
    __slots__ = ('__values', '__index')

    def __init__(self):
        self.__values = []
        self.__index = {}

    def __len__(self):
        return len(self.__values)

    def __repr__(self):
        return 'SampleSet(%r)' % (self.__values,)

    def add(self, value):
        assert value not in self.__index
        # Adding simply consists of adding the value to the end of the array
        # and updating the index.
        self.__index[value] = len(self.__values)
        self.__values.append(value)

    def remove(self, value):
        # To remove a value we first remove it from the index. But this leaves
        # us with the value still in the array, so we have to fix that. We
        # can't simply remove the value from the array, as that would a) Be an
        # O(n) operation and b) Leave the index completely wrong for every
        # value after that index.
        # So what we do is we take the last element of the array and place it
        # in the position of the value we just deleted (if the value was not
        # already the last element of the array. If it was then we don't have
        # to do anything extra). This reorders the array, but that's OK because
        # we don't care about its order, we just need to sample from it.
        i = self.__index.pop(value)
        last = self.__values.pop()
        if i < len(self.__values):
            self.__values[i] = last
            self.__index[last] = i

    def choice(self, random):
        return random.choice(self.__values)


class Negated(object):
    __slots__ = ('tag',)

    def __init__(self, tag):
        self.tag = tag


NEGATED_CACHE = {}


def negated(tag):
    try:
        return NEGATED_CACHE[tag]
    except KeyError:
        result = Negated(tag)
        NEGATED_CACHE[tag] = result
        return result


universal = UniqueIdentifier('universal')


class TargetSelector(object):
    """Data structure for selecting targets to use for mutation.

    The goal is to do a good job of exploiting novelty in examples without
    getting too obsessed with any particular novel factor.

    Roughly speaking what we want to do is give each distinct coverage target
    equal amounts of time. However some coverage targets may be harder to fuzz
    than others, or may only appear in a very small minority of examples, so we
    don't want to let those dominate the testing.

    Targets are selected according to the following rules:

    1. We ideally want valid examples as our starting point. We ignore
       interesting examples entirely, and other than that we restrict ourselves
       to the best example status we've seen so far. If we've only seen
       OVERRUN examples we use those. If we've seen INVALID but not VALID
       examples we use those. Otherwise we use VALID examples.
    2. Among the examples we've seen with the right status, when asked to
       select a target, we select a coverage target and return that along with
       an example exhibiting that target uniformly at random.

    Coverage target selection proceeds as follows:

    1. Whenever we return an example from select, we update the usage count of
       each of its tags.
    2. Whenever we see an example, we add it to the list of examples for all of
       its tags.
    3. When selecting a tag, we select one with a minimal usage count. Among
       those of minimal usage count we select one with the fewest examples.
       Among those, we select one uniformly at random.

    This has the following desirable properties:

    1. When two coverage targets are intrinsically linked (e.g. when you have
       multiple lines in a conditional so that either all or none of them will
       be covered in a conditional) they are naturally deduplicated.
    2. Popular coverage targets will largely be ignored for considering what
       test to run - if every example exhibits a coverage target, picking an
       example because of that target is rather pointless.
    3. When we discover new coverage targets we immediately exploit them until
       we get to the point where we've spent about as much time on them as the
       existing targets.
    4. Among the interesting deduplicated coverage targets we essentially
       round-robin between them, but with a more consistent distribution than
       uniformly at random, which is important particularly for short runs.

    """

    def __init__(self, random):
        self.random = random
        self.best_status = Status.OVERRUN
        self.reset()

    def reset(self):
        self.examples_by_tags = defaultdict(list)
        self.tag_usage_counts = Counter()
        self.tags_by_score = defaultdict(SampleSet)
        self.scores_by_tag = {}
        self.scores = []
        self.mutation_counts = 0
        self.example_counts = 0
        self.non_universal_tags = set()
        self.universal_tags = None

    def add(self, data):
        if data.status == Status.INTERESTING:
            return
        if data.status < self.best_status:
            return
        if data.status > self.best_status:
            self.best_status = data.status
            self.reset()

        if self.universal_tags is None:
            self.universal_tags = set(data.tags)
        else:
            not_actually_universal = self.universal_tags - data.tags
            for t in not_actually_universal:
                self.universal_tags.remove(t)
                self.non_universal_tags.add(t)
                self.examples_by_tags[t] = list(
                    self.examples_by_tags[universal]
                )

        new_tags = data.tags - self.non_universal_tags

        for t in new_tags:
            self.non_universal_tags.add(t)
            self.examples_by_tags[negated(t)] = list(
                self.examples_by_tags[universal]
            )

        self.example_counts += 1
        for t in self.tags_for(data):
            self.examples_by_tags[t].append(data)
            self.rescore(t)

    def has_tag(self, tag, data):
        if tag is universal:
            return True
        if isinstance(tag, Negated):
            return tag.tag not in data.tags
        return tag in data.tags

    def tags_for(self, data):
        yield universal
        for t in data.tags:
            yield t
        for t in self.non_universal_tags:
            if t not in data.tags:
                yield negated(t)

    def rescore(self, tag):
        new_score = (
            self.tag_usage_counts[tag], len(self.examples_by_tags[tag]))
        try:
            old_score = self.scores_by_tag[tag]
        except KeyError:
            pass
        else:
            self.tags_by_score[old_score].remove(tag)
        self.scores_by_tag[tag] = new_score

        sample = self.tags_by_score[new_score]
        if len(sample) == 0:
            heapq.heappush(self.scores, new_score)
        sample.add(tag)

    def select_tag(self):
        while True:
            peek = self.scores[0]
            sample = self.tags_by_score[peek]
            if len(sample) == 0:
                heapq.heappop(self.scores)
            else:
                return sample.choice(self.random)

    def select_example_for_tag(self, t):
        return self.random.choice(self.examples_by_tags[t])

    def select(self):
        t = self.select_tag()
        self.mutation_counts += 1
        result = self.select_example_for_tag(t)
        assert self.has_tag(t, result)
        for s in self.tags_for(result):
            self.tag_usage_counts[s] += 1
            self.rescore(s)
        return t, result


class Shrinker(object):
    """A shrinker is a child object of a ConjectureRunner which is designed to
    manage the associated state of a particular shrink problem.

    Currently the only shrink problem we care about is "interesting and with a
    particular interesting_origin", but this is abstracted into a general
    purpose predicate for more flexibility later - e.g. we are likely to want
    to shrink with respect to a particular coverage target later.

    Data with a status < VALID may be assumed not to satisfy the predicate.

    The expected usage pattern is that this is only ever called from within the
    engine.

    """

    def __init__(self, engine, initial, predicate):
        """Create a shrinker for a particular engine, with a given starting
        point and predicate. When shrink() is called it will attempt to find an
        example for which predicate is True and which is strictly smaller than
        initial.

        Note that initial is a ConjectureData object, and predicate
        takes ConjectureData objects.

        """
        self.__engine = engine
        self.__predicate = predicate
        self.__discarding_failed = False

        # We keep track of the current best example on the shrink_target
        # attribute.
        self.shrink_target = initial

    def incorporate_new_buffer(self, buffer):
        buffer = hbytes(buffer[:self.shrink_target.index])
        assert sort_key(buffer) < sort_key(self.shrink_target.buffer)

        if not self.__engine.prescreen_buffer(buffer):
            return False

        assert sort_key(buffer) <= sort_key(self.shrink_target.buffer)
        data = ConjectureData.for_buffer(buffer)
        self.__engine.test_function(data)
        result = self.incorporate_test_data(data)
        if result and not self.__discarding_failed:
            self.remove_discarded()
        return result

    def incorporate_test_data(self, data):
        if (
            self.__predicate(data) and
            sort_key(data.buffer) < sort_key(self.shrink_target.buffer)
        ):
            self.shrink_target = data
            return True
        return False

    def cached_test_function(self, buffer):
        result = self.__engine.cached_test_function(buffer)
        self.incorporate_test_data(result)
        return result

    def debug(self, msg):
        self.__engine.debug(msg)

    def greedy_shrink(self):
        # This will automatically be run during the normal loop, but it's worth
        # running once before the coarse passes so they don't spend time on
        # useless data.
        self.remove_discarded()

        # Coarse passes that are worth running once when the example is likely
        # to be "far from shrunk" but not worth repeating in a loop because
        # they are subsumed by more fine grained passes.
        self.delta_interval_deletion()
        self.coarse_block_replacement()

        prev = None
        while prev is not self.shrink_target:
            prev = self.shrink_target
            self.remove_discarded()
            self.minimize_duplicated_blocks()
            self.minimize_individual_blocks()
            self.reorder_blocks()
            self.greedy_interval_deletion()
            self.interval_deletion_with_block_lowering()

    def shrink(self):
        # We assume that if an all-zero block of bytes is an interesting
        # example then we're not going to do better than that.
        # This might not technically be true: e.g. for integers() | booleans()
        # the simplest example is actually [1, 0]. Missing this case is fairly
        # harmless and this allows us to make various simplifying assumptions
        # about the structure of the data (principally that we're never
        # operating on a block of all zero bytes so can use non-zeroness as a
        # signpost of complexity).
        if (
            not any(self.shrink_target.buffer) or
            self.incorporate_new_buffer(hbytes(len(self.shrink_target.buffer)))
        ):
            return

        self.greedy_shrink()
        self.escape_local_minimum()

    def escape_local_minimum(self):
        # The main shrink pass is purely greedy.
        # This is mostly pretty effective, but has a tendency
        # to get stuck in a local minimum in some cases.
        # So when we've completed the shrink process, we try
        # starting it again from something reasonably near to
        # the shrunk example that is likely to exhibit the same
        # behaviour. We then rerun the shrink process and see
        # if it gets a better result. If we do, we begin again.
        # If not, we bail out fairly quickly after a few tries
        # as this will usually not work.
        count = 0
        while count < 10:
            count += 1
            self.debug('Retrying from random restart')
            attempt_buf = bytearray(self.shrink_target.buffer)

            # We use the shrinking information to identify the
            # structural locations in the byte stream - if lowering
            # the block would result in changing the size of the
            # example, changing it here is too likely to break whatever
            # it was caused the behaviour we're trying to shrink.
            # Everything non-structural, we redraw uniformly at random.
            for i, (u, v) in enumerate(self.shrink_target.blocks):
                if i not in self.shrink_target.shrinking_blocks:
                    attempt_buf[u:v] = uniform(self.__engine.random, v - u)
            attempt = self.cached_test_function(attempt_buf)
            if self.__predicate(attempt):
                prev = self.shrink_target
                self.shrink_target = attempt
                self.greedy_shrink()
                if (
                    sort_key(self.shrink_target.buffer) <
                    sort_key(prev.buffer)
                ):
                    # We have successfully shrunk the example past where
                    # we started from. Now we begin the whole processs
                    # again from the new, smaller, example.
                    count = 0
                else:
                    self.shrink_target = prev

    def try_shrinking_blocks(self, blocks, b):
        initial_attempt = bytearray(self.shrink_target.buffer)
        for i in blocks:
            if i >= len(self.shrink_target.blocks):
                break
            u, v = self.shrink_target.blocks[i]
            initial_attempt[u:v] = b

        initial_data = self.cached_test_function(initial_attempt)

        if initial_data.status == Status.INTERESTING:
            return initial_data is self.shrink_target

        # If this produced something completely invalid we ditch it
        # here rather than trying to persevere.
        if initial_data.status < Status.VALID:
            return False

        if len(initial_data.buffer) < v:
            return False

        lost_data = len(self.shrink_target.buffer) - len(initial_data.buffer)

        # If this did not in fact cause the data size to shrink we
        # bail here because it's not worth trying to delete stuff from
        # the remainder.
        if lost_data <= 0:
            return False

        self.shrink_target.shrinking_blocks.update(blocks)

        try_with_deleted = bytearray(initial_attempt)
        del try_with_deleted[v:v + lost_data]

        if self.incorporate_new_buffer(try_with_deleted):
            return True

        return False

    def remove_discarded(self):
        """Try removing all bytes marked as discarded."""
        if not self.shrink_target.discarded:
            return
        attempt = bytearray(self.shrink_target.buffer)
        for u, v in sorted(self.shrink_target.discarded, reverse=True):
            del attempt[u:v]
        self.__discarding_failed = not self.incorporate_new_buffer(attempt)

    def delta_interval_deletion(self):
        """Attempt to delete every interval in the example."""

        self.debug('delta interval deletes')

        # We do a delta-debugging style thing here where we initially try to
        # delete many intervals at once and prune it down exponentially to
        # eventually only trying to delete one interval at a time.

        # I'm a little skeptical that this is helpful in general, but we've
        # got at least one benchmark where it does help.
        k = len(self.shrink_target.intervals) // 2
        while k > 0:
            i = 0
            while i + k <= len(self.shrink_target.intervals):
                bitmask = [True] * len(self.shrink_target.buffer)

                for u, v in self.shrink_target.intervals[i:i + k]:
                    for t in range(u, v):
                        bitmask[t] = False

                if not self.incorporate_new_buffer(hbytes(
                    b for b, v in zip(self.shrink_target.buffer, bitmask)
                    if v
                )):
                    i += k
            k //= 2

    def greedy_interval_deletion(self):
        """Attempt to delete every interval in the example."""
        self.debug('greedy interval deletes')
        i = 0
        while i < len(self.shrink_target.intervals):
            u, v = self.shrink_target.intervals[i]
            if not self.incorporate_new_buffer(
                self.shrink_target.buffer[:u] + self.shrink_target.buffer[v:]
            ):
                i += 1

    def coarse_block_replacement(self):
        """Attempts to zero every block. This is a very coarse pass that we
        only run once to attempt to remove some irrelevant detail. The main
        purpose of it is that if we manage to zero a lot of data then many
        attempted deletes become duplicates of each other, so we run fewer
        tests.

        If more blocks become possible to zero later that will be
        handled by minimize_individual_blocks. The point of this is
        simply to provide a fairly fast initial pass.

        """
        self.debug('Zeroing blocks')
        i = 0
        while i < len(self.shrink_target.blocks):
            buf = self.shrink_target.buffer
            u, v = self.shrink_target.blocks[i]
            assert u < v
            block = buf[u:v]
            if any(block):
                self.incorporate_new_buffer(buf[:u] + hbytes(v - u) + buf[v:])
            i += 1

    def minimize_duplicated_blocks(self):
        """Find blocks that have been duplicated in multiple places and attempt
        to minimize all of the duplicates simultaneously."""

        self.debug('Simultaneous shrinking of duplicated blocks')
        counts = Counter(
            self.shrink_target.buffer[u:v]
            for u, v in self.shrink_target.blocks
        )
        blocks = [buffer for buffer, count in counts.items() if count > 1]

        blocks.sort(reverse=True)
        blocks.sort(key=lambda b: counts[b] * len(b), reverse=True)
        for block in blocks:
            targets = [
                i for i, (u, v) in enumerate(self.shrink_target.blocks)
                if self.shrink_target.buffer[u:v] == block
            ]
            # This can happen if some blocks have been lost in the previous
            # shrinking.
            if len(targets) <= 1:
                continue

            minimize(
                block,
                lambda b: self.try_shrinking_blocks(targets, b),
                random=self.__engine.random, full=False
            )

    def minimize_individual_blocks(self):
        self.debug('Shrinking of individual blocks')
        i = 0
        while i < len(self.shrink_target.blocks):
            u, v = self.shrink_target.blocks[i]
            minimize(
                self.shrink_target.buffer[u:v],
                lambda b: self.try_shrinking_blocks((i,), b),
                random=self.__engine.random, full=False,
            )
            i += 1

    def reorder_blocks(self):
        self.debug('Reordering blocks')
        block_lengths = sorted(self.shrink_target.block_starts, reverse=True)
        for n in block_lengths:
            i = 1
            while i < len(self.shrink_target.block_starts.get(n, ())):
                j = i
                while j > 0:
                    buf = self.shrink_target.buffer
                    blocks = self.shrink_target.block_starts[n]
                    a_start = blocks[j - 1]
                    b_start = blocks[j]
                    a = buf[a_start:a_start + n]
                    b = buf[b_start:b_start + n]
                    if a <= b:
                        break
                    swapped = (
                        buf[:a_start] + b + buf[a_start + n:b_start] +
                        a + buf[b_start + n:])
                    assert len(swapped) == len(buf)
                    assert swapped < buf
                    if self.incorporate_new_buffer(swapped):
                        j -= 1
                    else:
                        break
                i += 1

    def interval_deletion_with_block_lowering(self):
        self.debug('Lowering blocks while deleting intervals')
        if not self.shrink_target.shrinking_blocks:
            return

        i = 0
        while i < len(self.shrink_target.intervals):
            u, v = self.shrink_target.intervals[i]
            changed = False
            prev = self.shrink_target
            # This loop never exits normally because the r >= u branch will
            # always trigger once we find a block inside the interval, hence
            # the pragma.
            for j, (r, s) in enumerate(  # pragma: no branch
                self.shrink_target.blocks
            ):
                if r >= u:
                    break
                if j not in self.shrink_target.shrinking_blocks:
                    continue
                b = self.shrink_target.buffer[r:s]
                if any(b):
                    n = int_from_bytes(b)

                    for m in hrange(max(n - 2, 0), n):
                        c = int_to_bytes(m, len(b))
                        attempt = bytearray(self.shrink_target.buffer)
                        attempt[r:s] = c
                        del attempt[u:v]
                        if self.incorporate_new_buffer(attempt):
                            self.shrink_target.shrinking_blocks.update(
                                k for k in prev.shrinking_blocks
                                if prev.blocks[k][-1] <= u
                            )
                            changed = True
                            break
                    if changed:
                        break
            if not changed:
                i += 1
