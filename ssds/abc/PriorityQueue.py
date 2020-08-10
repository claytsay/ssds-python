# -*- coding: utf-8 -*-
"""An abstract priority queue class.

This contains `PriorityQueue`, an abstract base class that serves as an
interface for extrinsic priority queues.
"""

from abc import ABC, abstractmethod


class PriorityQueue(ABC):
    """An interface for extrinsic priority queues.

    Priorities are independent of the objects being enqueued and must be
    supplied seperately.
    """
    @abstractmethod
    def __init__(self, is_max=False):
        """Constructs a priority queue.

        If the parameter 'isMax' is 'true', will be a maximum priority
        queue. If not, will default to a minimum priority queue.

        Args:
            is_max (:obj:`bool`, optional): Whether to make a maximum
                priority queue or not
        """
        pass

    @abstractmethod
    def add(self, item, priority: float) -> None:
        """Adds an item with the given priority value.

        Args:
            item: The item to add.
            priority (:obj:`float`): The priority of the item.
            
        Raises:
            ValueError: If the item is already present.
        """
        pass

    @abstractmethod
    def contains(self, item) -> bool:
        """Returns `True` if the priority queue contains the given item.

        Args:
            item: The item to test membership of.
            
        Returns:
            bool: `True` if the item is in the priority queue; `False`
            otherwise
        """
        pass

    @abstractmethod
    def get(self):
        """Returns the minimum or maximum item.

        Which (i.e. minimum or maximum) depends on if the priority queue was
        initialized as a minimum or maximum priority queue.

        Note:
            Does not remove the minimum/maximum item from the queue.
        
        Returns:
            The minimum or maximum item.
            
        Raises:
            RuntimeError: If the PQ is empty.
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """Returns the number of items in the priority queue.
        
        Returns:
            int: The number of items in the priority queue.
        """
        pass

    @abstractmethod
    def remove(self):
        """Removes and returns the minimum item.

        Which (i.e. minimum or maximum) depends on if the priority queue was
        initialized as a minimum or maximum priority queue.
        
        Returns:
            The minimum or maximum item.
        
        Raises:
            RuntimeError: If the PQ is empty.
        """
        pass

    @abstractmethod
    def change_priority(self, item, priority: float) -> None:
        """Changes the priority of the given item.
        
        Args:
            item: The item to modify the priority of.
            priority (:obj:`double`): The new priority to set `item` to.
        
        Raises:
            ValueError: If the item isn't in the queue.
        """
        pass
