# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""AVL Tree."""

from dataclasses import dataclass
from typing import Any, Optional

from forest import metrics
from forest import tree_exceptions


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

    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        self.root: Optional[Node] = None
        self._metrics_enabled = True if registry else False
        if self._metrics_enabled and registry:
            self._rotate_counter = metrics.Counter()
            self._height_histogram = metrics.Histogram()
            registry.register(name="avlt.rotate", metric=self._rotate_counter)
            registry.register(name="avlt.height", metric=self._height_histogram)

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
        new_node = Node(key=key, data=data)
        parent: Optional[Node] = None
        current: Optional[Node] = self.root
        while current:
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        # If the tree is empty, set the new node to be the root.
        if parent is None:
            self.root = new_node
        else:
            if new_node.key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node

            # After the insertion, fix the broken AVL-tree-property.
            # If the parent has two children after inserting the new node,
            # it means the parent had one child before the insertion.
            # In this case, neither AVL-tree property breaks nor
            # heights update requires.
            if not (parent.left and parent.right):
                self._insert_fixup(new_node)

        if self._metrics_enabled:
            self._height_histogram.update(value=self.get_height(self.root))

    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.

        Parameters
        ----------
        key: `Any`
            The key of the node to be deleted.
        """
        if self.root and (deleting_node := self.search(key=key)):

            # Case: no child
            if (deleting_node.left is None) and (deleting_node.right is None):
                self._delete_no_child(deleting_node=deleting_node)
            # Case: Two children
            elif deleting_node.left and deleting_node.right:
                replacing_node = self.get_leftmost(node=deleting_node.right)
                # Replace the deleting node with the replacing node,
                # but keep the replacing node in place.
                deleting_node.key = replacing_node.key
                deleting_node.data = replacing_node.data
                if replacing_node.right:  # The replacing node cannot have left child.
                    self._delete_one_child(deleting_node=replacing_node)
                else:
                    self._delete_no_child(deleting_node=replacing_node)
            # Case: one child
            else:
                self._delete_one_child(deleting_node=deleting_node)

            if self._metrics_enabled:
                self._height_histogram.update(value=self.get_height(self.root))

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
    def get_height(node: Optional[Node]) -> int:
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
        if node:
            return node.height
        # None has height -1
        return -1

    def _get_balance_factor(self, node: Optional[Node]) -> int:
        if node:
            return self.get_height(node.left) - self.get_height(node.right)
        # Empty node's height is -1
        return -1

    def _left_rotate(self, node_x: Node) -> None:
        node_y = node_x.right  # Set node y
        if node_y:
            # Turn node y's subtree into node x's subtree
            node_x.right = node_y.left
            if node_y.left:
                node_y.left.parent = node_x
            node_y.parent = node_x.parent

            # If node's parent is a Leaf, node y becomes the new root.
            if node_x.parent is None:
                self.root = node_y
            # Otherwise, update node x's parent.
            elif node_x == node_x.parent.left:
                node_x.parent.left = node_y
            else:
                node_x.parent.right = node_y

            node_y.left = node_x
            node_x.parent = node_y

            node_x.height = 1 + max(
                self.get_height(node_x.left), self.get_height(node_x.right)
            )
            node_y.height = 1 + max(
                self.get_height(node_y.left), self.get_height(node_y.right)
            )

            if self._metrics_enabled:
                self._rotate_counter.increase()

    def _right_rotate(self, node_x: Node) -> None:
        node_y = node_x.left  # Set node y
        if node_y:
            # Turn node y's subtree into node x's subtree
            node_x.left = node_y.right
            if node_y.right:
                node_y.right.parent = node_x
            node_y.parent = node_x.parent

            # If node's parent is a Leaf, node y becomes the new root.
            if node_x.parent is None:
                self.root = node_y
            # Otherwise, update node x's parent.
            elif node_x == node_x.parent.right:
                node_x.parent.right = node_y
            else:
                node_x.parent.left = node_y

            node_y.right = node_x
            node_x.parent = node_y

            node_x.height = 1 + max(
                self.get_height(node_x.left), self.get_height(node_x.right)
            )
            node_y.height = 1 + max(
                self.get_height(node_y.left), self.get_height(node_y.right)
            )

            if self._metrics_enabled:
                self._rotate_counter.increase()

    def _insert_fixup(self, new_node: Node) -> None:
        parent = new_node.parent

        while parent:
            parent.height = 1 + max(
                self.get_height(parent.left), self.get_height(parent.right)
            )

            grandparent = parent.parent
            # grandparent is unbalanced
            if grandparent:
                if self._get_balance_factor(grandparent) > 1:
                    # Case Left-Left
                    if self._get_balance_factor(parent) >= 0:
                        self._right_rotate(grandparent)
                    # Case Left-Right
                    elif self._get_balance_factor(parent) < 0:
                        self._left_rotate(parent)
                        self._right_rotate(grandparent)
                    # Since the fixup does not affect the ancestor of the unbalanced
                    # node, exit the loop to complete the fixup process.
                    break
                elif self._get_balance_factor(grandparent) < -1:
                    # Case Right-Right
                    if self._get_balance_factor(parent) <= 0:
                        self._left_rotate(grandparent)
                    # Case Right-Left
                    elif self._get_balance_factor(parent) > 0:
                        self._right_rotate(parent)
                        self._left_rotate(grandparent)
                    # Since the fixup does not affect the ancestor of the unbalanced
                    # node, exit the loop to complete the fixup process.
                    break
            parent = parent.parent

    def _delete_no_child(self, deleting_node: Node) -> None:
        parent = deleting_node.parent
        self._transplant(deleting_node=deleting_node, replacing_node=None)
        if parent:
            self._delete_fixup(fixing_node=parent)

    def _delete_one_child(self, deleting_node: Node) -> None:
        parent = deleting_node.parent
        replacing_node = (
            deleting_node.right if deleting_node.right else deleting_node.left
        )
        self._transplant(deleting_node=deleting_node, replacing_node=replacing_node)
        if parent:
            self._delete_fixup(fixing_node=parent)

    def _transplant(self, deleting_node: Node, replacing_node: Optional[Node]) -> None:
        if deleting_node.parent is None:
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        if replacing_node:
            replacing_node.parent = deleting_node.parent

    def _delete_fixup(self, fixing_node: Node) -> None:

        while fixing_node:
            fixing_node.height = 1 + max(
                self.get_height(fixing_node.left), self.get_height(fixing_node.right)
            )

            if self._get_balance_factor(fixing_node) > 1:
                # Case Left-Left
                if self._get_balance_factor(fixing_node.left) >= 0:
                    self._right_rotate(fixing_node)
                # Case Left-Right
                elif self._get_balance_factor(fixing_node.left) < 0:
                    # The fixing node's left child cannot be empty
                    self._left_rotate(fixing_node.left)  # type: ignore
                    self._right_rotate(fixing_node)

            elif self._get_balance_factor(fixing_node) < -1:
                # Case Right-Right
                if self._get_balance_factor(fixing_node.right) <= 0:
                    self._left_rotate(fixing_node)
                # Case Right-Left
                elif self._get_balance_factor(fixing_node.right) > 0:
                    # The fixing node's right child cannot be empty
                    self._right_rotate(fixing_node.right)  # type: ignore
                    self._left_rotate(fixing_node)

            fixing_node = fixing_node.parent  # type: ignore
