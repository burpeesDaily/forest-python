# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Thread-safe trees."""

import threading

from typing import Any, Optional

from forest import metrics
from forest.binary_trees import avl_tree
from forest.binary_trees import binary_search_tree
from forest.binary_trees import double_threaded_binary_tree
from forest.binary_trees import red_black_tree
from forest.binary_trees import single_threaded_binary_trees


class AVLTree(avl_tree.AVLTree):
    """Thread-safe AVL Tree."""

    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        avl_tree.AVLTree.__init__(self, registry=registry)
        self._lock = threading.Lock()

    def insert(self, key: Any, data: Any) -> None:
        """Thread-safe insert."""
        with self._lock:
            avl_tree.AVLTree.insert(self, key=key, data=data)

    def delete(self, key: Any) -> None:
        """Thread-safe delete."""
        with self._lock:
            avl_tree.AVLTree.delete(self, key=key)


class BinarySearchTree(binary_search_tree.BinarySearchTree):
    """Thread-safe Binary Search Tree."""

    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        binary_search_tree.BinarySearchTree.__init__(self, registry=registry)
        self._lock = threading.Lock()

    def insert(self, key: Any, data: Any) -> None:
        """Thread-safe insert."""
        with self._lock:
            binary_search_tree.BinarySearchTree.insert(self, key=key, data=data)

    def delete(self, key: Any) -> None:
        """Thread-safe delete."""
        with self._lock:
            binary_search_tree.BinarySearchTree.delete(self, key=key)


class RBTree(red_black_tree.RBTree):
    """Thread-safe Red-Black Tree."""

    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        red_black_tree.RBTree.__init__(self, registry=registry)
        self._lock = threading.Lock()

    def insert(self, key: Any, data: Any) -> None:
        """Thread-safe insert."""
        with self._lock:
            red_black_tree.RBTree.insert(self, key=key, data=data)

    def delete(self, key: Any) -> None:
        """Thread-safe delete."""
        with self._lock:
            red_black_tree.RBTree.delete(self, key=key)


class DoubleThreadedBinaryTree(double_threaded_binary_tree.DoubleThreadedBinaryTree):
    """Thread-safe Double Threaded Binary Search Tree."""

    def __init__(self) -> None:
        double_threaded_binary_tree.DoubleThreadedBinaryTree.__init__(self)
        self._lock = threading.Lock()

    def insert(self, key: Any, data: Any) -> None:
        """Thread-safe insert."""
        with self._lock:
            double_threaded_binary_tree.DoubleThreadedBinaryTree.insert(
                self, key=key, data=data
            )

    def delete(self, key: Any) -> None:
        """Thread-safe delete."""
        with self._lock:
            double_threaded_binary_tree.DoubleThreadedBinaryTree.delete(self, key=key)


class LeftThreadedBinaryTree(single_threaded_binary_trees.LeftThreadedBinaryTree):
    """Thread-safe Left Threaded Binary Search Tree."""

    def __init__(self) -> None:
        single_threaded_binary_trees.LeftThreadedBinaryTree.__init__(self)
        self._lock = threading.Lock()

    def insert(self, key: Any, data: Any) -> None:
        """Thread-safe insert."""
        with self._lock:
            single_threaded_binary_trees.LeftThreadedBinaryTree.insert(
                self, key=key, data=data
            )

    def delete(self, key: Any) -> None:
        """Thread-safe delete."""
        with self._lock:
            single_threaded_binary_trees.LeftThreadedBinaryTree.delete(self, key=key)


class RightThreadedBinaryTree(single_threaded_binary_trees.RightThreadedBinaryTree):
    """Thread-safe Right Threaded Binary Search Tree."""

    def __init__(self) -> None:
        single_threaded_binary_trees.RightThreadedBinaryTree.__init__(self)
        self._lock = threading.Lock()

    def insert(self, key: Any, data: Any) -> None:
        """Thread-safe insert."""
        with self._lock:
            single_threaded_binary_trees.RightThreadedBinaryTree.insert(
                self, key=key, data=data
            )

    def delete(self, key: Any) -> None:
        """Thread-safe delete."""
        with self._lock:
            single_threaded_binary_trees.RightThreadedBinaryTree.delete(self, key=key)
