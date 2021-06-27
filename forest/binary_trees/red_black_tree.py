# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Red-Black Tree."""

import enum

from dataclasses import dataclass

from typing import Any, Optional, Union

from forest import metrics
from forest import tree_exceptions
from forest.binary_trees import traversal


class Color(enum.Enum):
    """Color definition for Red-Black Tree."""

    RED = enum.auto()
    BLACK = enum.auto()


@dataclass
class Leaf:
    """Definition Red-Black Tree Leaf node whose color is always black."""

    color = Color.BLACK


@dataclass
class Node:
    """Red-Black Tree non-leaf node definition."""

    key: Any
    data: Any
    left: Union["Node", Leaf] = Leaf()
    right: Union["Node", Leaf] = Leaf()
    parent: Union["Node", Leaf] = Leaf()
    color: Color = Color.RED


class RBTree:
    """Red-Black Tree.

    Attributes
    ----------
    root: `Union[Node, Leaf]`
        The root node of the red-black tree.
    empty: `bool`
        `True` if the tree is empty; `False` otherwise.

    Methods
    -------
    Core Functions
    search(key: `Any`)
        Look for a node based on the given key.
    insert(key: `Any`, data: `Any`)
        Insert a (key, data) pair into a red-black tree.
    delete(key: `Any`)
        Delete a node based on the given key from the red-black tree.

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

    Traversal Function
    inorder_traverse()
        In-order traversal.
    preorder_traverse()
        Pre-order traversal.
    postorder_traverse()
        Post-order traversal.
    """

    def __init__(self, registry: Optional[metrics.MetricRegistry] = None) -> None:
        self._NIL: Leaf = Leaf()
        self.root: Union[Node, Leaf] = self._NIL
        self._metrics_enabled = True if registry else False
        if self._metrics_enabled and registry:
            self._rotate_counter = metrics.Counter()
            self._height_histogram = metrics.Histogram()
            registry.register(name="rbt.rotate", metric=self._rotate_counter)
            registry.register(name="rbt.height", metric=self._height_histogram)

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
        return self.root is self._NIL

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

        while isinstance(current, Node):
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:  # Key found
                return current
        # If the tree is empty (i.e., self.root == Leaf()), still return None.
        return None

    def insert(self, key: Any, data: Any) -> None:
        """Insert a (key, data) pair into the red-black tree.

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
        # Color the new node as red.
        new_node = Node(key=key, data=data, color=Color.RED)
        parent: Union[Node, Leaf] = self._NIL
        current: Union[Node, Leaf] = self.root
        while isinstance(current, Node):  # Look for the insert location
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        # If the parent is a Leaf, set the new node to be the root.
        if isinstance(parent, Leaf):
            new_node.color = Color.BLACK
            self.root = new_node
        else:
            if new_node.key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node

            # After the insertion, fix the broken red-black-tree-properties.
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
        if (deleting_node := self.search(key=key)) and (
            isinstance(deleting_node, Node)
        ):
            original_color = deleting_node.color

            # Case 1: no children or Case 2a: only one right child
            if isinstance(deleting_node.left, Leaf):
                replacing_node = deleting_node.right
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                # Fixup
                if original_color == Color.BLACK:
                    if isinstance(replacing_node, Node):
                        self._delete_fixup(fixing_node=replacing_node)

            # Case 2b: only one left child
            elif isinstance(deleting_node.right, Leaf):
                replacing_node = deleting_node.left
                self._transplant(
                    deleting_node=deleting_node, replacing_node=replacing_node
                )
                # Fixup
                if original_color == Color.BLACK:
                    if isinstance(replacing_node, Node):
                        self._delete_fixup(fixing_node=replacing_node)

            # Case 3: two children
            else:
                replacing_node = self.get_leftmost(deleting_node.right)
                original_color = replacing_node.color
                replacing_replacement = replacing_node.right
                # The replacing node is not the direct child of the deleting node
                if replacing_node.parent == deleting_node:
                    if isinstance(replacing_replacement, Node):
                        replacing_replacement.parent = replacing_node
                else:
                    self._transplant(replacing_node, replacing_node.right)
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = replacing_node

                self._transplant(deleting_node, replacing_node)
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = replacing_node
                replacing_node.color = deleting_node.color
                # Fixup
                if original_color == Color.BLACK:
                    if isinstance(replacing_replacement, Node):
                        self._delete_fixup(fixing_node=replacing_replacement)

            if self._metrics_enabled:
                self._height_histogram.update(value=self.get_height(self.root))

    @staticmethod
    def get_height(node: Union[Leaf, Node]) -> int:
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
        if isinstance(node, Node):
            if isinstance(node.left, Node) and isinstance(node.right, Node):
                return (
                    max(RBTree.get_height(node.left), RBTree.get_height(node.right)) + 1
                )

            if isinstance(node.left, Node):
                return RBTree.get_height(node=node.left) + 1

            if isinstance(node.right, Node):
                return RBTree.get_height(node=node.right) + 1

        return 0

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
        while isinstance(current_node.left, Node):
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
        while isinstance(current_node.right, Node):
            current_node = current_node.right
        return current_node

    @staticmethod
    def get_successor(node: Node) -> Union[Node, Leaf]:
        """Return the successor in the in-order order.

        Parameters
        ----------
        node: `Node`
            The node to get its successor.

        Returns
        -------
        `Union[Node, Leaf]`
            The successor node.
        """
        if isinstance(node.right, Node):  # Case 1: right child is not a leaf node.
            return RBTree.get_leftmost(node=node.right)
        # Case 2: right child is a leaf node.
        parent = node.parent
        while isinstance(parent, Node) and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def get_predecessor(node: Node) -> Union[Node, Leaf]:
        """Return the predecessor in the in-order order.

        Parameters
        ----------
        node: `Node`
            The node to get its predecessor.

        Returns
        -------
        `Union[Node, Leaf]`
            The predecessor node.
        """
        if isinstance(node.left, Node):
            return RBTree.get_rightmost(node=node.left)
        parent = node.parent
        while isinstance(parent, Node) and node == parent.left:
            node = parent
            parent = parent.parent
        return node.parent

    def inorder_traverse(self) -> traversal.Pairs:
        """Perform In-Order traversal.

        In-order traversal traverses a tree by the order:
        left subtree, current node, right subtree (LDR)

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the in-order traversal.
        """
        return self._inorder_traverse(node=self.root)

    def preorder_traverse(self) -> traversal.Pairs:
        """Perform Pre-Order traversal.

        Pre-order traversal traverses a tree by the order:
        current node, left subtree, right subtree (DLR)

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the pre-order traversal.
        """
        return self._preorder_traverse(node=self.root)

    def postorder_traverse(self) -> traversal.Pairs:
        """Perform Post-Order traversal.

        Post-order traversal traverses a tree by the order:
        left subtree, right subtree, current node (LRD)

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the post-order traversal.
        """
        return self._postorder_traverse(node=self.root)

    def _left_rotate(self, node_x: Node) -> None:
        node_y = node_x.right  # Set node y
        if isinstance(node_y, Leaf):  # Node y cannot be a Leaf
            raise RuntimeError("Invalid left rotate")

        # Turn node y's subtree into node x's subtree
        node_x.right = node_y.left
        if isinstance(node_y.left, Node):
            node_y.left.parent = node_x
        node_y.parent = node_x.parent

        # If node's parent is a Leaf, node y becomes the new root.
        if isinstance(node_x.parent, Leaf):
            self.root = node_y
        # Otherwise, update node x's parent.
        elif node_x == node_x.parent.left:
            node_x.parent.left = node_y
        else:
            node_x.parent.right = node_y

        node_y.left = node_x
        node_x.parent = node_y

        if self._metrics_enabled:
            self._rotate_counter.increase()

    def _right_rotate(self, node_x: Node) -> None:
        node_y = node_x.left  # Set node y
        if isinstance(node_y, Leaf):  # Node y cannot be a Leaf
            raise RuntimeError("Invalid right rotate")
        # Turn node y's subtree into node x's subtree
        node_x.left = node_y.right
        if isinstance(node_y.right, Node):
            node_y.right.parent = node_x
        node_y.parent = node_x.parent

        # If node's parent is a Leaf, node y becomes the new root.
        if isinstance(node_x.parent, Leaf):
            self.root = node_y
        # Otherwise, update node x's parent.
        elif node_x == node_x.parent.right:
            node_x.parent.right = node_y
        else:
            node_x.parent.left = node_y

        node_y.right = node_x
        node_x.parent = node_y

        if self._metrics_enabled:
            self._rotate_counter.increase()

    def _insert_fixup(self, fixing_node: Node) -> None:
        while fixing_node.parent.color == Color.RED:
            if fixing_node.parent == fixing_node.parent.parent.left:  # type: ignore
                parent_sibling = fixing_node.parent.parent.right  # type: ignore
                if parent_sibling.color == Color.RED:  # Case 1
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    fixing_node = fixing_node.parent.parent  # type: ignore
                else:
                    # Case 2
                    if fixing_node == fixing_node.parent.right:  # type: ignore
                        fixing_node = fixing_node.parent  # type: ignore
                        self._left_rotate(fixing_node)
                    # Case 3
                    fixing_node.parent.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    self._right_rotate(fixing_node.parent.parent)  # type: ignore
            else:
                parent_sibling = fixing_node.parent.parent.left  # type: ignore
                if parent_sibling.color == Color.RED:  # Case 4
                    fixing_node.parent.color = Color.BLACK
                    parent_sibling.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    fixing_node = fixing_node.parent.parent  # type: ignore
                else:
                    # Case 5
                    if fixing_node == fixing_node.parent.left:  # type: ignore
                        fixing_node = fixing_node.parent  # type: ignore
                        self._right_rotate(fixing_node)
                    # Case 6
                    fixing_node.parent.color = Color.BLACK
                    fixing_node.parent.parent.color = Color.RED  # type: ignore
                    self._left_rotate(fixing_node.parent.parent)  # type: ignore

        self.root.color = Color.BLACK

    def _delete_fixup(self, fixing_node: Union[Leaf, Node]) -> None:
        while (fixing_node is not self.root) and (fixing_node.color == Color.BLACK):
            if fixing_node == fixing_node.parent.left:  # type: ignore
                sibling = fixing_node.parent.right  # type: ignore

                # Case 1: the sibling is red.
                if sibling.color == Color.RED:
                    sibling.color == Color.BLACK
                    fixing_node.parent.color = Color.RED  # type: ignore
                    self._left_rotate(fixing_node.parent)  # type: ignore
                    sibling = fixing_node.parent.right  # type: ignore

                if isinstance(sibling, Leaf):
                    break

                # Case 2: the sibling is black and its children are black.
                if (sibling.left.color == Color.BLACK) and (  # type: ignore
                    sibling.right.color == Color.BLACK  # type: ignore
                ):
                    sibling.color = Color.RED
                    # new fixing node
                    fixing_node = fixing_node.parent  # type: ignore

                # Cases 3 and 4: the sibling is black and one of
                # its child is red and the other is black.
                else:
                    # Case 3: the sibling is black and its left child is red.
                    if sibling.right.color == Color.BLACK:  # type: ignore
                        sibling.left.color = Color.BLACK  # type: ignore
                        sibling.color = Color.RED  # type: ignore
                        self._right_rotate(node_x=sibling)  # type: ignore

                    # Case 4: the sibling is black and its right child is red.
                    sibling.color = fixing_node.parent.color  # type: ignore
                    fixing_node.parent.color = Color.BLACK  # type: ignore
                    sibling.right.color = Color.BLACK  # type: ignore
                    self._left_rotate(node_x=fixing_node.parent)  # type: ignore
                    # Once we are here, all the violation has been fixed, so
                    # move to the root to terminate the loop.
                    fixing_node = self.root
            else:
                sibling = fixing_node.parent.left  # type: ignore

                # Case 5: the sibling is red.
                if sibling.color == Color.RED:
                    sibling.color == Color.BLACK  # type: ignore
                    fixing_node.parent.color = Color.RED  # type: ignore
                    self._right_rotate(node_x=fixing_node.parent)  # type: ignore
                    sibling = fixing_node.parent.left  # type: ignore

                if isinstance(sibling, Leaf):
                    break

                # Case 6: the sibling is black and its children are black.
                if (sibling.right.color == Color.BLACK) and (  # type: ignore
                    sibling.left.color == Color.BLACK  # type: ignore
                ):
                    sibling.color = Color.RED
                    fixing_node = fixing_node.parent  # type: ignore
                else:
                    # Case 7: the sibling is black and its right child is red.
                    if sibling.left.color == Color.BLACK:  # type: ignore
                        sibling.right.color = Color.BLACK  # type: ignore
                        sibling.color = Color.RED
                        self._left_rotate(node_x=sibling)  # type: ignore
                    # Case 8: the sibling is black and its left child is red.
                    sibling.color = fixing_node.parent.color  # type: ignore
                    fixing_node.parent.color = Color.BLACK  # type: ignore
                    sibling.left.color = Color.BLACK  # type: ignore
                    self._right_rotate(node_x=fixing_node.parent)  # type: ignore
                    # Once we are here, all the violation has been fixed, so
                    # move to the root to terminate the loop.
                    fixing_node = self.root

        fixing_node.color = Color.BLACK

    def _transplant(
        self, deleting_node: Node, replacing_node: Union[Node, Leaf]
    ) -> None:
        if isinstance(deleting_node.parent, Leaf):
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        if isinstance(replacing_node, Node):
            replacing_node.parent = deleting_node.parent

    def _inorder_traverse(self, node: Union[Node, Leaf]) -> traversal.Pairs:
        if isinstance(node, Node):
            yield from self._inorder_traverse(node.left)
            yield (node.key, node.data)
            yield from self._inorder_traverse(node.right)

    def _preorder_traverse(self, node: Union[Node, Leaf]) -> traversal.Pairs:
        if isinstance(node, Node):
            yield (node.key, node.data)
            yield from self._preorder_traverse(node.left)
            yield from self._preorder_traverse(node.right)

    def _postorder_traverse(self, node: Union[Node, Leaf]) -> traversal.Pairs:
        if isinstance(node, Node):
            yield from self._postorder_traverse(node.left)
            yield from self._postorder_traverse(node.right)
            yield (node.key, node.data)
