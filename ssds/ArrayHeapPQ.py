# -*- coding: utf-8 -*-
"""Contains a heap-based priority queue implementation.

Uses an array to store the contents of the heap. Should have O(log(n))
adds, removes, and updates.
"""

from enum import Enum
from ssds.abc.PriorityQueue import PriorityQueue


class _Relation(Enum):
    PARENT = 'PARENT'
    CHILD_LEFT = 'CHILD_LEFT'
    CHILD_RIGHT = 'CHILD_RIGHT'


class ArrayHeapPQ(PriorityQueue):

    # = = = = = = = = = = = = =
    # CONSTRUCTOR
    # = = = = = = = = = = = = =

    def __init__(self, is_max=False):
        super().__init__(is_max)
        self._nodes = [None]
        self._locations = {}
        self._max = is_max

    # = = = = = = = = = = = = =
    # PUBLIC METHODS
    # = = = = = = = = = = = = =

    def add(self, item, priority: float) -> None:
        if self.contains(item):
            # TODO: Maybe change this to simply update the priority?
            raise ValueError('item already present')
        if self._max:
            priority *= -1
        self._nodes.append((item, priority))
        self._locations[item] = len(self._nodes) - 1
        self._swim(len(self._nodes) - 1)

    def contains(self, item) -> bool:
        return item in self._locations.keys()

    def get(self):
        self._validateSize()
        return self._nodes[1][0]

    def remove(self):
        self._validateSize()
        smallest = None
        if self.size() == 1:
            smallest = self._nodes.pop(1)
        else:
            self._swap(1, len(self._nodes) - 1)
            smallest = self._nodes.pop(len(self._nodes) - 1)
            self._swim(1)

        self._locations.pop(smallest[0])
        return smallest[0]

    def size(self) -> int:
        return len(self._locations)

    def changePriority(self, item, priority: float) -> None:
        index = self._locations.get(item, None)
        if index is None:
            raise ValueError('item %s does not exist' % str(item))
        if self._max:
            priority *= -1
        self._nodes[index] = (self._nodes[index][0], priority)
        self._swim(index)

    # = = = = = = = = = = = = =
    # PRIVATE METHODS
    # = = = = = = = = = = = = =

    # - - - - - - - - - - - - -
    # Parent/Child Utility Methods
    # - - - - - - - - - - - - -

    def _hasRelation(self, index: int, relation: _Relation) -> bool:
        """Checks to see whether a node has a certain relation.

        Determines whether the node at the given index has a given relation
        or not. If the provided Relation is invalid, will return `False` by
        default.

        Args:
            index (:obj:`int`): The index whose relation is to be queried.
            relation (:obj:`Relation`): The relation to be queried about.

        Returns:
            bool: `True` if the relation node exists, `False` otherwise.
        """
        if relation is _Relation.PARENT:
            return self._getRelationIndex(index, relation) != 0
        elif relation is _Relation.CHILD_LEFT:
            return self._isValidIndex(self._getRelationIndex(index, relation))
        elif relation is _Relation.CHILD_RIGHT:
            return self._isValidIndex(self._getRelationIndex(index, relation))
        else:
            return False

    def _getRelationIndex(self, index: int, relation: _Relation) -> int:
        """Gets the index of the specified relation.

        If the given Relation is invalid, returns 0.

        Note:
            Might return an out-of-bounds index. 

        Args:
            index (:obj:`int`): The index whose relation's index is to be
                queried.
            relation (:obj:`Relation`): The relation to be queried about.

        Returns:
            int: The index of the specified relation of the given index.
        """

        if relation is _Relation.PARENT:
            return index // 2
        elif relation is _Relation.CHILD_LEFT:
            return index * 2 + 1
        elif relation is _Relation.CHILD_RIGHT:
            return index * 2
        else:
            return 0

    def _getRelationPriority(self, index: int, relation: _Relation) -> float:
        """Gets the priority value of the specified relation.

        Note:
            If the relation is invalid (e.g. does not exist), will return 
            positive infinity for the priority.

        Args:
            index (:obj:`int`): The index whose relation's priority is to
                be queried.
            relation (:obj:`Relation`): The relation to be queried about.

        Returns:
            float: The priority value of the specified relation to the
            given index.
        """
        if not self._hasRelation(index, relation):
            return float('inf')
        else:
            return self._nodes[self._getRelationIndex(index, relation)][1]

    def _shouldSwap(self, index: int, relation: _Relation) -> bool:
        """Determines if the node should be swapped with its relation.

        The method will return 'true' if the relation exists and comparison
        of the priorities shows that the two should be swapped.

        Args:
            index (:obj:`int`): The index whose relation's "swappiness" is
                to be queried.
            relation (:obj:`Relation`): The relation to be queried about.

        Returns:
            bool: `True` if the node should be swapped with its relation;
            `False` otherwise.
        """
        nodePriority = self._nodes[index][1]
        relationPriority = self._getRelationPriority(index, relation)
        if self._hasRelation(index, relation):
            if relation is _Relation.PARENT:
                return nodePriority < relationPriority
            else:
                return nodePriority > relationPriority
        else:
            return False

    # - - - - - - - - - - - - -
    # Heap Manipulation Methods
    # - - - - - - - - - - - - -

    def _swap(self, i: int, j: int) -> None:
        """Swaps the items at the specified indices of the list.

        Also updates the locations dictionary with the new indices.

        Args:
            i (:obj:`int`): The index of one of the items to swap.
            j (:obj:`int`): The index of the other item to swap.
        """

        self._nodes[i], self._nodes[j] = self._nodes[j], self._nodes[i]
        iKey = self._nodes[i][0]
        jKey = self._nodes[j][0]
        tempIndex_i = self._locations[iKey]
        tempIndex_j = self._locations[jKey]
        self._locations[iKey] = tempIndex_j
        self._locations[jKey] = tempIndex_i

    def _swim(self, index: int) -> None:
        """Attempts to swim a node to its correct position.

        Args:
            index (:obj:`int`): The index of the node to swim.
        """
        if self._shouldSwap(index, _Relation.PARENT):
            swapIndex = self._getRelationIndex(index, _Relation.PARENT)
            self._swap(index, swapIndex)
            self._swim(swapIndex)
        elif self._shouldSwap(index,
                              _Relation.CHILD_LEFT) or self._shouldSwap(
            index, _Relation.CHILD_RIGHT):
            leftPriority = self._getRelationPriority(index,
                                                     _Relation.CHILD_LEFT)
            rightPriority = self._getRelationPriority(index,
                                                      _Relation.CHILD_RIGHT)
            if rightPriority < leftPriority:
                swapIndex = self._getRelationIndex(index,
                                                   _Relation.CHILD_RIGHT)
                self._swap(index, swapIndex)
                self._swim(swapIndex)
            else:
                swapIndex = self._getRelationIndex(index, _Relation.CHILD_LEFT)
                self._swap(index, swapIndex)
                self._swim(swapIndex)

    # - - - - - - - - - - - - -
    # Miscellaneous Utility Methods
    # - - - - - - - - - - - - -

    def _isValidIndex(self, index: int) -> bool:
        """Checks whether an index is acceptable or not.

        Checks to verify that (a) the index is within the bounds of the 
        list, and (b) the reference at the index is not null.

        Args:
            index (:obj:`int`): The index to check acceptability of.

        Returns:
            bool: `True` if the index is acceptable; `False` otherwise.
        """
        return 0 <= index < len(self._nodes) and self._nodes[index] is not None

    def _validateSize(self) -> None:
        """Checks to see if the size of the queue is greater than zero.

        Raises:
            RuntimeError: If the size of the queue <= 0.
        """
        if self.size() == 0:
            # TODO: Change this error
            raise RuntimeError('queue has size zero')
