# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""AVL Tree."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    """AVL Tree node definition."""

    key: Any
    data: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    height: int = 0


class AVLTree:
    """AVL Tree.

    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the AVL tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    Core Functions
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into an AVL tree.
    delete(key: `Any`)
        Delete a node based on the given key from the AVL tree.

    Auxiliary Functions
    get_leftmost(node: `Node`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `Node` = `None`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `Node`)
        Return the successor node in the in-order order.
    get_predecessor(node: `Node`)
        Return the predecessor node in the in-order order.
    get_height(node: `Union[Node, Leaf]`)
        Return the height of the given node.
    """

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def __repr__(self) -> str:
        """Provie the tree representation to visualize its layout."""
        if self.root:
            return (
                f"{type(self)}, root={self.root}, "
                f"tree_height={str(self.get_height(self.root))}"
            )
        return "empty tree"

    @property
    def empty(self) -> bool:
        """bool: `True` if the tree is empty; `False` otherwise.

        Notes
        -----
        The property, `empty`, is read-only.
        """
        return self.root is None

    def search(self, key: Any) -> Optional[Node]:
        """Look for a node by a given key.

        Parameters
        ----------
        key: `Any`
            The key associated with the node.

        Returns
        -------
        `Optional[Node]`
            The node found by the given key.
        If the key does not exist, return `None`.
        """
        current = self.root

        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:  # Key found
                return current
        return None

    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the AVL tree.

        Parameters
        ----------
        key: `Any`
            The key associated with the data.

        data: `Any`
            The data to be inserted.

        Raises
        ------
        `DuplicateKeyError`
            Raised if the key to be insted has existed in the tree.
        """
        pass

    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.

        Parameters
        ----------
        key: `Any`
            The key of the node to be deleted.
        """
        pass

    @staticmethod
    def get_leftmost(node: Node) -> Node:
        """Return the leftmost node from a given subtree.

        The key of the leftmost node is the smallest key in the given subtree.

        Parameters
        ----------
        node: `Node`
            The root of the subtree.

        Returns
        -------
        `Node`
            The node whose key is the smallest from the subtree of
            the given node.
        """
        current_node = node
        while current_node.left:
            current_node = current_node.left
        return current_node

    @staticmethod
    def get_rightmost(node: Node) -> Node:
        """Return the rightmost node from a given subtree.

        The key of the rightmost node is the biggest key in the given subtree.

        Parameters
        ----------
        node: `Node`
            The root of the subtree.

        Returns
        -------
        `Node`
            The node whose key is the biggest from the subtree of
            the given node.
        """
        current_node = node
        while current_node.right:
            current_node = current_node.right
        return current_node

    @staticmethod
    def get_successor(node: Node) -> Optional[Node]:
        """Return the successor in the in-order order.

        Parameters
        ----------
        node: `Node`
            The node to get its successor.

        Returns
        -------
        `Optional[Node]`
            The successor node.
        """
        if node.right:  # Case 1: right child is not empty
            return AVLTree.get_leftmost(node=node.right)
        # Case 2: right child is empty
        parent = node.parent
        while parent and (node == parent.right):
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def get_predecessor(node: Node) -> Optional[Node]:
        """Return the predecessor in the in-order order.

        Parameters
        ----------
        node: `Node`
            The node to get its predecessor.

        Returns
        -------
        `Optional[Node]`
            The predecessor node.
        """
        if node.left:  # Case 1: left child is not empty
            return AVLTree.get_rightmost(node=node.left)
        # Case 2: left child is empty
        parent = node.parent
        while parent and (node == parent.left):
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def get_height(node: Node) -> int:
        """Get the height of the given subtree.

        Parameters
        ----------
        node: `Node`
            The root of the subtree to get its height.

        Returns
        -------
        `int`
            The height of the given subtree. 0 if the subtree has only one node.
        """
        return node.height
