# -*- coding: utf-8 -*-
from enum import Enum
from ssds.abc.PriorityQueue import PriorityQueue


class _Relation(Enum):
    PARENT = 'PARENT'
    CHILD_LEFT = 'CHILD_LEFT'
    CHILD_RIGHT = 'CHILD_RIGHT'


class ArrayHeapPQ(PriorityQueue):
    """Array-Heap Priority Queue.

    Uses an array to store the contents of the heap. Should have
    :math:`\\mathcal{O}(\\log(n))` adds, removes, and updates.

    Parameters
    ----------
    is_max : bool, default=False
        Selects whether the priority queue should dequeue the item with
        the maximum priority (instead of the minimum priority).

    Examples
    --------
    >>> from ssds import ArrayHeapPQ
    >>> pq = ArrayHeapPQ()
    >>> pq.add('a', 1)
    >>> pq.add('b', 2)
    >>> pq.change_priority('b', 0)
    >>> pq.remove()
    'b'
    """

    # = = = = = = = = = = = = =
    # CONSTRUCTOR
    # = = = = = = = = = = = = =

    def __init__(self, is_max=False):
        """Initialize self. See help(type(self)) for accurate signature."""

        super().__init__(is_max)
        self._nodes = [None]
        self._locations = {}
        self._max = is_max

    # = = = = = = = = = = = = =
    # PUBLIC METHODS
    # = = = = = = = = = = = = =

    def add(self, item, priority: float) -> None:
        """Adds an item to the priority queue.

        Parameters
        ----------
        item
            An item to be inserted into the queue. Does not need to be
            hashable.

        priority : float
            The extrinsic priority of the object.
            
        Returns
        -------
        None
            Nothing.
        """
        # TODO: Assess whether an infinitely positive/negative priority
        #   would cause the code to malfunction
        if self.contains(item):
            # TODO: Maybe change this to simply update the priority?
            raise ValueError('item already present')
        if self._max:
            priority *= -1
        self._nodes.append((item, priority))
        self._locations[item] = len(self._nodes) - 1
        self._swim(len(self._nodes) - 1)

    def contains(self, item) -> bool:
        """Returns whether the item is in the priority queue or not.

        Parameters
        ----------
        item
            An item to test the membership of in the priority queue.
            
        Returns
        -------
        bool
            Returns True if `item` is in the priority queue;
            False otherwise.
        """
        return item in self._locations.keys()

    def get(self):
        """Returns the first item in the priority queue.

        Which (i.e. minimum or maximum) depends on if the priority queue was
        initialized as a minimum or maximum priority queue. Does not remove
        the minimum/maximum item from the queue.

        Parameters
        ----------
        N/A

        Returns
        -------
        object
            The foremost item in the priority queue.
        """
        self._validateSize()
        return self._nodes[1][0]

    def remove(self):
        """Removes and returns the first item in the priority queue.

        Which (i.e. minimum or maximum) depends on if the priority queue was
        initialized as a minimum or maximum priority queue.

        Parameters
        ----------
        N/A

        Returns
        -------
        object
            The foremost item in the priority queue.
        """
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
        """Returns the number of items in the priority queue.

        Parameters
        ----------
        N/A

        Returns
        -------
        int
            The number of items in the priority queue.
        """
        return len(self._locations)

    def change_priority(self, item, priority: float) -> None:
        """Changes the priority of the given item.

        Parameters
        ----------
        item : any
            The item in the priority queue to modify the priority of.

        priority : double
            The new priority to set the item to.

        Returns
        -------
        None
            Nothing.
        """
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

    def _has_relation(self, index: int, relation: _Relation) -> bool:
        """Checks to see whether a node has a certain relation.

        Determines whether the node at the given index has a given relation
        or not. If the provided Relation is invalid, will return `False` by
        default.

        Parameters
        ----------
        index : int
            The index whose relation is to be queried.

        relation : ssds.ArrayHeapPQ._Relation
            The relation to be queried about.

        Returns
        -------
        bool
            True if the relation node exists, False otherwise.
        """
        if relation is _Relation.PARENT:
            return self._get_relation_index(index, relation) != 0
        elif relation is _Relation.CHILD_LEFT:
            return self._is_valid_index(self._get_relation_index(index, relation))
        elif relation is _Relation.CHILD_RIGHT:
            return self._is_valid_index(self._get_relation_index(index, relation))
        else:
            return False

    def _get_relation_index(self, index: int, relation: _Relation) -> int:
        """Gets the index of the specified relation.

        If the given Relation is invalid, returns 0.

        Notes
        -----
        Might return an out-of-bounds index.

        Parameters
        ----------
        index : int
            The index whose relation's index is to be queried.

        relation : ssds.ArrayHeapPQ._Relation
            The relation to be queried about.

        Returns
        -------
        int
            The index of the specified relation of the given index.
        """
        if relation is _Relation.PARENT:
            return index // 2
        elif relation is _Relation.CHILD_LEFT:
            return index * 2 + 1
        elif relation is _Relation.CHILD_RIGHT:
            return index * 2
        else:
            return 0

    def _get_relation_priority(self, index: int, relation: _Relation) -> float:
        """Gets the priority value of the specified relation.

        Notes
        -----
        If the relation is invalid (e.g. does not exist), will return
        positive infinity for the priority.

        Parameters
        ----------
        index : int
            The index whose relation's priority is to be queried.

        relation : ssds.ArrayHeapPQ._Relation
            The relation to be queried about.

        Returns
        -------
        float
            The priority value of the specified relation to the given index.
        """
        if not self._has_relation(index, relation):
            return float('inf')
        else:
            return self._nodes[self._get_relation_index(index, relation)][1]

    def _should_swap(self, index: int, relation: _Relation) -> bool:
        """Determines if the node should be swapped with its relation.

        The method will return 'true' if the relation exists and comparison
        of the priorities shows that the two should be swapped.

        Parameters
        ----------
        index : int
            The index whose relation's "swappiness" is to be queried.

        relation : ssds.ArrayHeapPQ._Relation
            The relation to be queried about.

        Returns
        -------
        bool
            True if the node should be swapped with its relation;
            False otherwise.
        """
        nodePriority = self._nodes[index][1]
        relationPriority = self._get_relation_priority(index, relation)
        if self._has_relation(index, relation):
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

        Parameters
        ----------
        i : int
            The index of one of the items to swap.

        j : int
            The index of the other item to swap.
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

        Parameters
        ----------
        index : int
            The index of the node to swim.
        """
        if self._should_swap(index, _Relation.PARENT):
            swapIndex = self._get_relation_index(index, _Relation.PARENT)
            self._swap(index, swapIndex)
            self._swim(swapIndex)
        elif self._should_swap(index,
                               _Relation.CHILD_LEFT) or self._should_swap(
            index, _Relation.CHILD_RIGHT):
            leftPriority = self._get_relation_priority(index,
                                                       _Relation.CHILD_LEFT)
            rightPriority = self._get_relation_priority(index,
                                                        _Relation.CHILD_RIGHT)
            if rightPriority < leftPriority:
                swapIndex = self._get_relation_index(index,
                                                     _Relation.CHILD_RIGHT)
                self._swap(index, swapIndex)
                self._swim(swapIndex)
            else:
                swapIndex = self._get_relation_index(index, _Relation.CHILD_LEFT)
                self._swap(index, swapIndex)
                self._swim(swapIndex)

    # - - - - - - - - - - - - -
    # Miscellaneous Utility Methods
    # - - - - - - - - - - - - -

    def _is_valid_index(self, index: int) -> bool:
        """Checks whether an index is acceptable or not.

        Checks to verify that (a) the index is within the bounds of the 
        list, and (b) the reference at the index is not null.

        Parameters
        ----------
        index : int
            The index to check acceptability of.

        Returns
        -------
        bool
            True if `index` is acceptable; False otherwise.
        """
        return 0 <= index < len(self._nodes) and self._nodes[index] is not None

    def _validateSize(self) -> None:
        """Checks to see if the size of the queue is greater than zero.

        Notes
        -----
        Raises a RuntimeError if the size of the queue <= 0.
        """
        if self.size() == 0:
            # TODO: Change this error
            raise RuntimeError('queue has size zero')
