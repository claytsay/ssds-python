# -*- coding: utf-8 -*-
"""Contains a reference priority queue implementation.

The reference priority queue is slow (O(n) complexity), but works. Used to
assess other implementations of priority queues.
"""

from ssds.abc.PriorityQueue import PriorityQueue


class ReferencePQ(PriorityQueue):
    """A reference implementation of a priority queue.

    Inefficient, but works. Used to verify integrity and evaluate performance
    of better priority queue implementations.
    """

    def __init__(self, is_max=False):
        super().__init__(is_max)
        self._nodes = []
        self._max = is_max

    def add(self, item, priority: float) -> None:
        if self.contains(item):
            raise ValueError('item already present')
        if self._max:
            priority *= -1
        self._nodes.append((item, priority))

    def contains(self, item) -> bool:
        for item2, priority in self._nodes:
            if item2 == item:
                return True
        return False

    def get(self):
        if self.size() == 0:
            raise RuntimeError('queue is empty')
        return min(self._nodes, key=lambda x: x[1])[0]

    def remove(self):
        if self.size() == 0:
            raise RuntimeError('queue is empty')
        index = self._indexOf(self.get())
        return self._nodes.pop(index)[0]

    def change_priority(self, item, priority: float) -> None:
        if not self.contains(item):
            raise ValueError('item not in queue')
        if self._max:
            priority *= -1
        self._nodes[self._indexOf(item)] = (self._nodes[self._indexOf(item)][0], priority)

    def size(self) -> int:
        return len(self._nodes)

    def _indexOf(self, item) -> int:
        for i in range(len(self._nodes)):
            if self._nodes[i][0] == item:
                return i
        raise ValueError('item not in queue')
