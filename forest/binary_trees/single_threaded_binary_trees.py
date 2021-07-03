# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Single Threaded Binary Search Trees."""

import dataclasses

from typing import Any, Optional

from forest.binary_trees import traversal
from forest import tree_exceptions


@dataclasses.dataclass
class Node:
    """Single Threaded Tree node definition."""

    key: Any
    data: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    is_thread: bool = False


class RightThreadedBinaryTree:
    """Right Threaded Binary Tree.

    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the right threaded binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    Core Functions
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into a binary tree.
    delete(key: `Any`)
        Delete a node based on the given key from the binary tree.

    Auxiliary Functions
    get_leftmost(node: `Node`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `Node` = `None`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `Node`)
        Return the successor node in the in-order order.
    get_predecessor(node: `Node`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[Node]`)
        Return the height of the given node.

    Traversal Functions
    inorder_traverse()
        In-order traversal by using the right threads.
    preorder_traverse()
        Pre-order traversal by using the right threads.
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
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:  # key > current.key
                if current.is_thread:
                    break
                current = current.right
        return None

    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the binary search tree.

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
        new_node = Node(key=key, data=data)
        parent: Optional[Node] = None
        current: Optional[Node] = self.root

        while current:
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                # If the node is thread, meaning it's a leaf node.
                if current.is_thread:
                    current = None
                else:
                    current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        # If the tree is empty
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node

            # Update thread
            new_node.right = parent
            new_node.is_thread = True

        else:
            # Update thread
            new_node.is_thread = parent.is_thread
            new_node.right = parent.right
            parent.is_thread = False
            # Parent's right must be set after thread update
            parent.right = new_node

    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.

        Parameters
        ----------
        key: `Any`
            The key of the node to be deleted.
        """
        if self.root and (deleting_node := self.search(key=key)):

            # Case 1: no child
            if deleting_node.left is None and (
                deleting_node.right is None or deleting_node.is_thread
            ):
                self._transplant(deleting_node=deleting_node, replacing_node=None)

            # Case 2a: only one right child
            elif deleting_node.left is None and deleting_node.is_thread is False:
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )

            # Case 2b: only one left child
            elif deleting_node.left and deleting_node.is_thread:
                predecessor = self.get_predecessor(node=deleting_node)
                if predecessor:
                    predecessor.right = deleting_node.right
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )

            # Case 3: two children
            elif (
                deleting_node.left
                and deleting_node.right
                and deleting_node.is_thread is False
            ):
                predecessor = self.get_predecessor(node=deleting_node)
                replacing_node: Node = self.get_leftmost(node=deleting_node.right)
                # the leftmost node is not the direct child of the deleting node
                if replacing_node.parent != deleting_node:
                    if replacing_node.is_thread:
                        self._transplant(
                            deleting_node=replacing_node, replacing_node=None
                        )
                    else:
                        self._transplant(
                            deleting_node=replacing_node,
                            replacing_node=replacing_node.right,
                        )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node
                    replacing_node.is_thread = False

                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                if predecessor and predecessor.is_thread:
                    predecessor.right = replacing_node
            else:
                raise RuntimeError("Invalid case. Should never happened")

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

        while current_node.is_thread is False and current_node.right:
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
        if node.is_thread:
            return node.right
        else:
            if node.right:
                return RightThreadedBinaryTree.get_leftmost(node=node.right)
            # if node.right is None, it means no successor of the given node.
            return None

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
        if node.left:
            return RightThreadedBinaryTree.get_rightmost(node=node.left)
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def get_height(node: Optional[Node]) -> int:
        """Get the height of the given subtree.

        Parameters
        ----------
        node: `Optional[Node]`
            The root of the subtree to get its height.

        Returns
        -------
        `int`
            The height of the given subtree. 0 if the subtree has only one node.
        """
        if node:
            if node.left and node.is_thread is False:
                return (
                    max(
                        RightThreadedBinaryTree.get_height(node.left),
                        RightThreadedBinaryTree.get_height(node.right),
                    )
                    + 1
                )

            if node.left:
                return RightThreadedBinaryTree.get_height(node=node.left) + 1

            if node.is_thread is False:
                return RightThreadedBinaryTree.get_height(node=node.right) + 1
        return 0

    def inorder_traverse(self) -> traversal.Pairs:
        """Use the right threads to traverse the tree in in-order order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree in-order traversal.
        """
        if self.root:
            current: Optional[Node] = self.get_leftmost(node=self.root)
            while current:
                yield (current.key, current.data)

                if current.is_thread:
                    current = current.right
                else:
                    if current.right is None:
                        break
                    current = self.get_leftmost(current.right)

    def preorder_traverse(self) -> traversal.Pairs:
        """Use the right threads to traverse the tree in pre-order order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree pre-order traversal.
        """
        current = self.root
        while current:
            yield (current.key, current.data)

            if current.is_thread:
                # If a node is thread, it must have a right child.
                current = current.right.right  # type: ignore
            else:
                current = current.left

    def _transplant(self, deleting_node: Node, replacing_node: Optional[Node]) -> None:
        if deleting_node.parent is None:
            self.root = replacing_node
            if self.root:
                self.root.is_thread = False
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
            if replacing_node:
                if deleting_node.is_thread:
                    if replacing_node.is_thread:
                        replacing_node.right = replacing_node.right
        else:  # deleting_node == deleting_node.parent.right
            deleting_node.parent.right = replacing_node
            if replacing_node:
                if deleting_node.is_thread:
                    if replacing_node.is_thread:
                        replacing_node.right = replacing_node.right
            else:
                deleting_node.parent.right = deleting_node.right
                deleting_node.parent.is_thread = True

        if replacing_node:
            replacing_node.parent = deleting_node.parent


class LeftThreadedBinaryTree:
    """Left Threaded Binary Tree.

    Attributes
    ----------
    root: `Optional[Node]`
        The root node of the left threaded binary search tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    Core Functions
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into a binary tree.
    delete(key: `Any`)
        Delete a node based on the given key from the binary tree.

    Auxiliary Functions
    get_leftmost(node: `Node`)
        Return the node whose key is the smallest from the given subtree.
    get_rightmost(node: `Node` = `None`)
        Return the node whose key is the biggest from the given subtree.
    get_successor(node: `Node`)
        Return the successor node in the in-order order.
    get_predecessor(node: `Node`)
        Return the predecessor node in the in-order order.
    get_height(node: `Optional[Node]`)
        Return the height of the given node.

    Traversal Function
    reverse_inorder_traverse()
        Reversed In-order traversal by using the left threads.
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
            if key == current.key:
                return current
            elif key < current.key:
                if current.is_thread is False:
                    current = current.left
                else:
                    break
            else:  # key > current.key:
                current = current.right
        return None

    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the binary search tree.

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
        new_node = Node(key=key, data=data)
        parent: Optional[Node] = None
        current: Optional[Node] = self.root

        while current:
            parent = current
            if new_node.key < current.key:
                # If the node is thread, meaning it's a leaf node.
                if current.is_thread:
                    current = None
                else:
                    current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        # If the tree is empty
        if parent is None:
            self.root = new_node
        elif new_node.key > parent.key:
            parent.right = new_node

            # Update thread
            new_node.left = parent
            new_node.is_thread = True

        else:
            # Update thread
            new_node.is_thread = parent.is_thread
            new_node.left = parent.left
            parent.is_thread = False
            # Parent's left must be set after thread update
            parent.left = new_node

    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.

        Parameters
        ----------
        key: `Any`
            The key of the node to be deleted.
        """
        if self.root and (deleting_node := self.search(key=key)):

            # Case 1: no child
            if deleting_node.right is None and (
                deleting_node.left is None or deleting_node.is_thread
            ):
                self._transplant(deleting_node=deleting_node, replacing_node=None)

            # Case 2a: only one right child
            elif deleting_node.right and deleting_node.is_thread:
                successor = self.get_successor(node=deleting_node)
                if successor:
                    successor.left = deleting_node.left
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.right
                )

            # Case 2b: only one left left child
            elif (deleting_node.right is None) and (deleting_node.is_thread is False):
                self._transplant(
                    deleting_node=deleting_node, replacing_node=deleting_node.left
                )

            # Case 3: two children
            elif deleting_node.right and deleting_node.left:
                replacing_node: Node = self.get_leftmost(node=deleting_node.right)
                successor = self.get_successor(node=replacing_node)
                # the minmum node is not the direct child of the deleting node
                if replacing_node.parent != deleting_node:
                    if replacing_node.is_thread:
                        self._transplant(
                            deleting_node=replacing_node, replacing_node=None
                        )
                    else:
                        self._transplant(
                            deleting_node=replacing_node,
                            replacing_node=replacing_node.right,
                        )
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node

                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                replacing_node.is_thread = False
                if successor and successor.is_thread:
                    successor.left = replacing_node
            else:
                raise RuntimeError("Invalid case. Should never happened")

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

        while current_node.left and current_node.is_thread is False:
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
        if node.right:
            return LeftThreadedBinaryTree.get_leftmost(node=node.right)
        parent = node.parent
        while parent and node == parent.right:
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
        if node.is_thread:
            return node.left
        else:
            if node.left:
                return LeftThreadedBinaryTree.get_rightmost(node=node.left)
            # if node.left is None, it means no predecessor of the given node.
            return None

    @staticmethod
    def get_height(node: Optional[Node]) -> int:
        """Get the height of the given subtree.

        Parameters
        ----------
        node: `Optional[Node]`
            The root of the subtree to get its height.

        Returns
        -------
        `int`
            The height of the given subtree. 0 if the subtree has only one node.
        """
        if node:
            if node.right and node.is_thread is False:
                return (
                    max(
                        LeftThreadedBinaryTree.get_height(node.left),
                        LeftThreadedBinaryTree.get_height(node.right),
                    )
                    + 1
                )

            if node.right:
                return LeftThreadedBinaryTree.get_height(node=node.right) + 1

            if node.is_thread is False:
                return LeftThreadedBinaryTree.get_height(node=node.left) + 1

        return 0

    def reverse_inorder_traverse(self) -> traversal.Pairs:
        """Use the left threads to traverse the tree in reversed in-order.

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the tree reversed in-order traversal.
        """
        if self.root:
            current: Optional[Node] = self.get_rightmost(node=self.root)
            while current:
                yield (current.key, current.data)

                if current.is_thread:
                    current = current.left
                else:
                    if current.left is None:
                        break
                    current = self.get_rightmost(current.left)

    def _transplant(self, deleting_node: Node, replacing_node: Optional[Node]) -> None:
        if deleting_node.parent is None:
            self.root = replacing_node
            if self.root:
                self.root.is_thread = False
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
            if replacing_node:
                if deleting_node.is_thread:
                    if replacing_node.is_thread:
                        replacing_node.left = deleting_node.left
            else:
                deleting_node.parent.left = deleting_node.left
                deleting_node.parent.is_thread = True
        else:  # deleting_node == deleting_node.parent.right
            deleting_node.parent.right = replacing_node
            if replacing_node:
                if deleting_node.is_thread:
                    if replacing_node.is_thread:
                        replacing_node.left = deleting_node.left

        if replacing_node:
            replacing_node.parent = deleting_node.parent
