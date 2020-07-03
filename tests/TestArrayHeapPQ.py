# -*- coding: utf-8 -*-
"""Used to test the `ArrayHeapPQ`.

Contains a mixture of non-randomized and randomized testing. In addition,
some tests measure the performance of the data structure.
"""

import unittest
from enum import Enum
from math import floor, log2
from random import choice, random, randrange
from time import perf_counter

from ssds import ArrayHeapPQ
from ssds.reference import ReferencePQ

_MAX_VAL = 1000
"""int: Represents the maximum value that can be added."""

_MAX_PRIORITY = 1000
"""int: The maximum priority that can be assigned."""


class _Method(Enum):
    ADD = 0
    CONTAINS = 1
    GET_SMALLEST = 2
    REMOVE_SMALLEST = 3
    SIZE = 4
    CHANGE_PRIORITY = 5


class TestArrayHeapPQ(unittest.TestCase):

    # = = = = = = = = = = = = =
    # TESTS
    # = = = = = = = = = = = = =

    def test_basic(self):
        """A basic test.
        
        Note:
            This test is meant to be used with a debugger to see what
            happens inside the ArrayHeapMinPQ.
        """
        ahpq = ArrayHeapPQ()

        for i in range(6):
            ahpq.add(i, i)
        for i in range(6):
            self.assertEqual(i, ahpq.remove())

    def test_random(self):
        ahpq = ArrayHeapPQ()
        npq = ReferencePQ()
        vals = {}
        val = 0
        priority = None

        for i in range(100_000):
            j = randrange(0, 5)
            if j == 0:  # add
                val = randrange(_MAX_VAL)
                priority = random() * _MAX_PRIORITY
                if npq.contains(val):
                    with self.assertRaises(ValueError):
                        ahpq.add(val, priority)
                else:
                    ahpq.add(val, priority)
                    npq.add(val, priority)
                    vals[val] = priority
            elif j == 1:  # contains
                if random() < 0.5:
                    # Test item not in vals
                    val = randrange(_MAX_VAL)
                    while val in vals:
                        val = randrange(_MAX_VAL)
                elif len(vals) > 0:
                    # Test item in vals
                    val = choice(list(vals.keys()))
                else:
                    continue
                self.assertEqual(npq.contains(val), ahpq.contains(val))
            elif j == 2:  # get
                if npq.size() == 0:
                    with self.assertRaises(RuntimeError):
                        ahpq.get()
                else:
                    self.assertEqual(npq.get(), ahpq.get())
            elif j == 3:  # remove
                if npq.size() == 0:
                    with self.assertRaises(RuntimeError):
                        ahpq.remove()
                else:
                    vals.pop(npq.get())
                    self.assertEqual(npq.remove(), ahpq.remove())
            elif j == 4:  # size
                self.assertEqual(npq.size(), ahpq.size())
            elif j == 5:  # changePriority
                priority = random() * _MAX_PRIORITY
                val = choice(val.keys())
                npq.changePriority(val, priority)
                ahpq.changePriority(val, priority)
            else:
                continue

    def test_time(self):
        # Test parameters
        maxOps = 5000
        numTrials = 6

        # Other variables
        header = ' numOps   | add      | contains | size     | getSmall | removeSm | changePr '
        hline = '----------+----------+----------+----------+----------+----------+----------'
        times = {}
        times[_Method.GET_SMALLEST] = 0.0
        times[_Method.REMOVE_SMALLEST] = 0.0
        times[_Method.CHANGE_PRIORITY] = 0.0

        # Do the timing and print as well
        print('', hline, header, hline, sep='\n')
        for num_ops in [10 * (2 ** x) for x in range(floor(log2(maxOps // 10)))]:
            num_ops_str = ''
            self._time_part1(num_ops, numTrials, times)
            self._time_part2(num_ops, numTrials, times)
            num_ops_str += ' %8d ' % num_ops
            for m in _Method:
                num_ops_str += '| %8f ' % times[m]
            print(num_ops_str)

    # = = = = = = = = = = = = =
    # PRIVATE UTILITY METHODS
    # = = = = = = = = = = = = =

    def _time_part1(self, numOps: int, numTrials: int, times: dict) -> None:
        """Tests the speed of the `add`, `contains`, and `size` methods.

        Args:
            numOps (:obj:`int`): The number of operations to perform per trial.
            numTrials (:obj:`int`): The number of trials to perform.
            times (:obj:`dict`): The data structure which to update with the average
                time across the trials.
        """

        ahpq = None
        trialTimes = [[0] * numTrials for _ in range(3)]
        startTime = None
        endTime = None

        for trial in range(numTrials):
            ahpq = ArrayHeapPQ()

            # add
            startTime = perf_counter()
            for _ in range(numOps):
                try:
                    ahpq.add(randrange(numOps * 2), random() * _MAX_PRIORITY)
                except ValueError:
                    continue
            endTime = perf_counter()
            trialTimes[0][trial] = endTime - startTime

            # contains
            startTime = perf_counter()
            for _ in range(numOps):
                ahpq.contains(randrange(numOps))
            endTime = perf_counter()
            trialTimes[1][trial] = endTime - startTime

            # size
            startTime = perf_counter()
            for _ in range(numOps):
                ahpq.size()
            endTime = perf_counter()
            trialTimes[2][trial] = endTime - startTime

        # Get summary statistics
        times[_Method.ADD] = sum(trialTimes[0]) / numTrials
        times[_Method.CONTAINS] = sum(trialTimes[1]) / numTrials
        times[_Method.SIZE] = sum(trialTimes[2]) / numTrials

    def _time_part2(self, numOps: int, numTrials: int, times: dict) -> None:
        """Tests the speed of `get`, `remove`, and `changePriority`.

        Args:
            numOps (:obj:`int`): The number of operations to perform.
            numTrials (:obj:`int`): The number of trials to perform.
            times (:obj:`dict`): The data structure which to update with the average
                time across the trials.
        """
        ahpq = None
        trialTimes = [[0] * numTrials for _ in range(3)]
        values = set()
        startTime = None
        endTime = None

        for trial in range(numTrials):
            # Set up the priority queue
            ahpq = ArrayHeapPQ()
            for _ in range(numOps):
                self.add_to_pq(ahpq, values, numOps * 10)

            # get
            startTime = perf_counter()
            for _ in range(numOps):
                ahpq.get()
            endTime = perf_counter()
            trialTimes[0][trial] = endTime - startTime

            # remove
            removeTimes = [0] * numOps
            removed = None
            for i in range(numOps):
                # Time the operation
                startTime = perf_counter()
                removed = ahpq.remove()
                endTime = perf_counter()
                removeTimes[i] = endTime - startTime

                # "Reset" PQ.
                values.remove(removed)
                self.add_to_pq(ahpq, values, numOps * 10)
            trialTimes[1][trial] = sum(removeTimes) / numOps

            # changePriority
            cpTimes = [0] * numOps
            for i in range(numOps):
                value = choice(list(values))
                startTime = perf_counter()
                ahpq.changePriority(value, random() * _MAX_PRIORITY)
                endTime = perf_counter()
                cpTimes[i] = endTime - startTime
            trialTimes[2][trial] = sum(cpTimes) / numOps
            values.clear()

        times[_Method.GET_SMALLEST] = sum(trialTimes[0]) / numTrials
        times[_Method.REMOVE_SMALLEST] = sum(trialTimes[1]) / numTrials
        times[_Method.CHANGE_PRIORITY] = sum(trialTimes[2]) / numTrials

    @staticmethod
    def add_to_pq(pq, s: set, upper: float) -> None:
        """Adds a value to the specified priority queue.

        If a duplicate value is attempted to be added, will keep on trying to add
        values until a value is finally added. Uses MAX_PRIORITY to determine
        the maximum possible priority.

        Args:
            pq: The priority queue to add the value to.
            s (:obj:`set`): The set of values in the priority queue.
            upper (:obj:`float`): The maximum value to add.
        """
        value = None
        while True:
            value = randrange(upper)
            if value not in s:
                pq.add(value, random() * _MAX_PRIORITY)
                s.add(value)
                return


if __name__ == '__main__':
    unittest.main()
