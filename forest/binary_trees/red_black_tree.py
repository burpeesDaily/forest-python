# Copyright © 2021 by Shun Huang. All rights reserved.
# Licensed under MIT License.
# See LICENSE in the project root for license information.

"""Red-Black Tree."""

import enum

from dataclasses import dataclass

from typing import Any, Optional, Union

from forest.binary_trees import traversal


class Color(enum.Enum):
    """Color definition for Red-Black Tree."""

    Red = enum.auto()
    Black = enum.auto()


@dataclass
class LeafNode:
    """Definition Red-Black Tree Leaf node whose color is always black."""

    color = Color.Black


@dataclass
class Node:
    """Red-Black Tree non-leaf node definition."""

    key: Any
    data: Any
    left: Union["Node", LeafNode]
    right: Union["Node", LeafNode]
    parent: Union["Node", LeafNode]
    color: Color = Color.Red


class RBTree:
    """Red-Black Tree.

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
    inorder_traverse()
        In-order traversal.
    preorder_traverse()
        Pre-order traversal.
    postorder_traverse()
        Post-order traversal.
    """

    def __init__(self) -> None:
        self._NIL: LeafNode = LeafNode()
        self.root: Union[Node, LeafNode] = self._NIL

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
        temp: Union[Node, LeafNode] = self.root
        while isinstance(temp, Node):
            if key < temp.key:
                temp = temp.left
            elif key > temp.key:
                temp = temp.right
            else:  # Key found
                return temp
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
        node = Node(key=key, data=data, left=self._NIL, right=self._NIL, parent=self._NIL, color=Color.Red)  # Color the new node as red.
        parent: Union[Node, LeafNode] = self._NIL
        temp: Union[Node, LeafNode] = self.root
        while isinstance(temp, Node):  # Look for the insert location
            parent = temp
            if node.key < temp.key:
                temp = temp.left
            else:
                temp = temp.right
        # If the parent is a LeafNode, set the new node to be the root.
        if isinstance(parent, LeafNode):
            node.color = Color.Black
            self.root = node
        else:
            node.parent = parent

            if node.key < parent.key:
                parent.left = node
            else:
                parent.right = node

            # After the insertion, fix the broken red-black-tree-properties.
            self._insert_fixup(node)

    def delete(self, key: Any) -> None:
        """Delete a node according to the given key.

        Parameters
        ----------
        key: `Any`
            The key of the node to be deleted.
        """
        deleting_node: Node = self.search(key=key)

        original_color = deleting_node.color

        # No children or only one right child
        if isinstance(deleting_node.left, LeafNode):
            replacing_node = deleting_node.right
            self._transplant(deleting_node=deleting_node,
                             replacing_node=replacing_node)
            # Fixup
            if original_color == Color.Black:
                if isinstance(replacing_node, Node):
                    self._delete_fixup(fixing_node=replacing_node)

        # Only one left child
        elif isinstance(deleting_node.right, LeafNode):
            replacing_node = deleting_node.left
            self._transplant(deleting_node=deleting_node,
                             replacing_node=replacing_node)
            # Fixup
            if original_color == Color.Black:
                self._delete_fixup(fixing_node=replacing_node)

        # Two children
        else:
            replacing_node = self.get_leftmost(deleting_node.right)
            original_color = replacing_node.color
            replacing_replacement = replacing_node.right
            # The replacing node is not the direct child of the deleting node
            if replacing_node.parent != deleting_node:
                self._transplant(replacing_node, replacing_node.right)
                replacing_node.right = deleting_node.right
                replacing_node.right.parent = replacing_node

            self._transplant(deleting_node, replacing_node)
            replacing_node.left = deleting_node.left
            replacing_node.left.parent = replacing_node
            replacing_node.color = deleting_node.color
            # Fixup
            if original_color == Color.Black:
                if isinstance(replacing_replacement, Node):
                    self._delete_fixup(fixing_node=replacing_replacement)

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
    def get_successor(node: Node) -> Union[Node, LeafNode]:
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
        if isinstance(node.right, Node):
            return RBTree.get_leftmost(node=node.right)
        parent = node.parent
        while isinstance(parent, Node) and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def get_predecessor(node: Node) -> Union[Node, LeafNode]:
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
        if isinstance(node.left, Node):
            return RBTree.get_rightmost(node=node.left)
        parent = node.parent
        while isinstance(parent, Node) and node == parent.left:
            node = parent
            parent = parent.parent
        return node.parent

    @staticmethod
    def get_height(node: Union[None, LeafNode, Node]) -> int:
        """Return the height of the given node.

        See Also
        --------
        :py:meth:`pyforest.binary_trees.binary_tree.BinaryTree.get_height`.
        """
        if node is None:
            return 0

        if isinstance(node.left, LeafNode) and \
           isinstance(node.right, LeafNode):
            return 0

        return max(RBTree.get_height(node.left),
                   RBTree.get_height(node.right)) + 1

    def inorder_traverse(self) -> traversal.Pairs:
        """Perform In-Order traversal.

        In-order traversal traverses a tree by the order:
        left subtree, current node, right subtree (LDR)

        Yields
        ------
        `Pairs`
            The next (key, data) pair in the in-order traversal.

        Examples
        --------
        >>> from pyforest.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
        >>> tree.insert(key=23, data="23")
        >>> tree.insert(key=4, data="4")
        >>> tree.insert(key=30, data="30")
        >>> tree.insert(key=11, data="11")
        >>> tree.insert(key=7, data="7")
        >>> tree.insert(key=34, data="34")
        >>> tree.insert(key=20, data="20")
        >>> tree.insert(key=24, data="24")
        >>> tree.insert(key=22, data="22")
        >>> tree.insert(key=15, data="15")
        >>> tree.insert(key=1, data="1")
        >>> [item for item in tree.preorder_traverse()]
        [(1, '1'), (4, '4'), (7, '7'), (11, '11'), (15, '15'), (20, '20'),
        (22, '22'), (23, '23'), (24, '24'), (30, '30'), (34, '34')]
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

        Examples
        --------
        >>> from pyforest.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
        >>> tree.insert(key=23, data="23")
        >>> tree.insert(key=4, data="4")
        >>> tree.insert(key=30, data="30")
        >>> tree.insert(key=11, data="11")
        >>> tree.insert(key=7, data="7")
        >>> tree.insert(key=34, data="34")
        >>> tree.insert(key=20, data="20")
        >>> tree.insert(key=24, data="24")
        >>> tree.insert(key=22, data="22")
        >>> tree.insert(key=15, data="15")
        >>> tree.insert(key=1, data="1")
        >>> [item for item in tree.preorder_traverse()]
        [(20, "20"), (7, "7"), (4, "4"), (1, "1"), (11, "11"), (15, "15"),
        (23, "23"), (22, "22"), (30, "30"), (24, "24"), (34, "34")]
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

        Examples
        --------
        >>> from pyforest.binary_trees import red_black_tree
        >>> tree = red_black_tree.RBTree()
        >>> tree.insert(key=23, data="23")
        >>> tree.insert(key=4, data="4")
        >>> tree.insert(key=30, data="30")
        >>> tree.insert(key=11, data="11")
        >>> tree.insert(key=7, data="7")
        >>> tree.insert(key=34, data="34")
        >>> tree.insert(key=20, data="20")
        >>> tree.insert(key=24, data="24")
        >>> tree.insert(key=22, data="22")
        >>> tree.insert(key=15, data="15")
        >>> tree.insert(key=1, data="1")
        >>> [item for item in tree.postorder_traverse()]
        [(1, "1"), (4, "4"), (15, "15"), (11, "11"), (7, "7"), (22, "22"),
        (24, "24"), (34, "34"), (30, "30"), (23, "23"), (20, "20")]
        """
        return self._postorder_traverse(node=self.root)

    def _left_rotate(self, node_x: Node) -> None:
        node_y = node_x.right  # Set node y
        if isinstance(node_y, LeafNode):  # Node y cannot be a LeafNode
            raise RuntimeError("Invalid left rotate")

        # Turn node y's subtree into node x's subtree
        node_x.right = node_y.left
        if isinstance(node_y.left, Node):
            node_y.left.parent = node_x
        node_y.parent = node_x.parent

        # If node's parent is a LeafNode, node y becomes the new root.
        if isinstance(node_x.parent, LeafNode):
            self.root = node_y
        # Otherwise, update node x's parent.
        elif node_x == node_x.parent.left:
            node_x.parent.left = node_y
        else:
            node_x.parent.right = node_y

        node_y.left = node_x
        node_x.parent = node_y

    def _right_rotate(self, node_x: Node) -> None:
        node_y = node_x.left  # Set node y
        if isinstance(node_y, LeafNode):  # Node y cannot be a LeafNode
            raise RuntimeError("Invalid right rotate")
        # Turn node y's subtree into node x's subtree
        node_x.left = node_y.right
        if isinstance(node_y.right, Node):
            node_y.right.parent = node_x
        node_y.parent = node_x.parent

        # If node's parent is a LeafNode, node y becomes the new root.
        if isinstance(node_x.parent, LeafNode):
            self.root = node_y
        # Otherwise, update node x's parent.
        elif node_x == node_x.parent.right:
            node_x.parent.right = node_y
        else:
            node_x.parent.left = node_y

        node_y.right = node_x
        node_x.parent = node_y

    def _insert_fixup(self, fixing_node: Node) -> None:
        while fixing_node.parent.color == Color.Red:
            if fixing_node.parent == fixing_node.parent.parent.left:
                parent_sibling = fixing_node.parent.parent.right
                if parent_sibling.color == Color.Red:  # Case 1
                    fixing_node.parent.color = Color.Black
                    parent_sibling.color = Color.Black
                    fixing_node.parent.parent.color = Color.Red
                    fixing_node = fixing_node.parent.parent
                else:
                    # Case 2
                    if fixing_node == fixing_node.parent.right:
                        fixing_node = fixing_node.parent
                        self._left_rotate(fixing_node)
                    # Case 3
                    fixing_node.parent.color = Color.Black
                    fixing_node.parent.parent.color = Color.Red
                    self._right_rotate(fixing_node.parent.parent)
            else:
                parent_sibling = fixing_node.parent.parent.left
                if parent_sibling.color == Color.Red:  # Case 4
                    fixing_node.parent.color = Color.Black
                    parent_sibling.color = Color.Black
                    fixing_node.parent.parent.color = Color.Red
                    fixing_node = fixing_node.parent.parent
                else:
                    # Case 5
                    if fixing_node == fixing_node.parent.left:
                        fixing_node = fixing_node.parent
                        self._right_rotate(fixing_node)
                    # Case 6
                    fixing_node.parent.color = Color.Black
                    fixing_node.parent.parent.color = Color.Red
                    self._left_rotate(fixing_node.parent.parent)

        self.root.color = Color.Black

    def _delete_fixup(self, fixing_node: Union[LeafNode, Node]) -> None:
        while (fixing_node is not self.root) and \
              (fixing_node.color == Color.Black):
            if fixing_node == fixing_node.parent.left:
                sibling = fixing_node.parent.right

                # Case 1: the sibling is red.
                if sibling.color == Color.Red:
                    sibling.color == Color.Black
                    fixing_node.parent.color = Color.Red
                    self._left_rotate(fixing_node.parent)
                    sibling = fixing_node.parent.right

                # Case 2: the sibling is black and its children are black.
                if (sibling.left.color == Color.Black) and \
                   (sibling.right.color == Color.Black):
                    sibling.color = Color.Red
                    fixing_node = fixing_node.parent # new fixing node

                # Cases 3 and 4: the sibling is black and one of
                # its child is red and the other is black.
                else:
                    # Case 3: the sibling is black and its left child is red.
                    if sibling.right.color == Color.Black:
                        sibling.left.color = Color.Black
                        sibling.color = Color.Red
                        self._right_rotate(node_x=sibling)

                    # Case 4: the sibling is black and its right child is red.
                    sibling.color = fixing_node.parent.color
                    fixing_node.parent.color = Color.Black
                    sibling.right.color = Color.Black
                    self._left_rotate(node_x=fixing_node.parent)
                    # Once we are here, all the violation has been fixed, so
                    # move to the root to terminate the loop.
                    fixing_node = self.root
            else:
                sibling = fixing_node.parent.left

                # Case 5: the sibling is red.
                if sibling.color == Color.Red:
                    sibling.color == Color.Black
                    fixing_node.parent.color = Color.Red
                    self._right_rotate(node_x=fixing_node.parent)
                    sibling = fixing_node.parent.left

                # Case 6: the sibling is black and its children are black.
                if (sibling.right.color == Color.Black) and \
                   (sibling.left.color == Color.Black):
                    sibling.color = Color.Red
                    fixing_node = fixing_node.parent
                else:
                    # Case 7: the sibling is black and its right child is red.
                    if sibling.left.color == Color.Black:
                        sibling.right.color = Color.Black
                        sibling.color = Color.Red
                        self._left_rotate(node_x=sibling)
                    # Case 8: the sibling is black and its left child is red.
                    sibling.color = fixing_node.parent.color
                    fixing_node.parent.color = Color.Black
                    sibling.left.color = Color.Black
                    self._right_rotate(node_x=fixing_node.parent)
                    # Once we are here, all the violation has been fixed, so
                    # move to the root to terminate the loop.
                    fixing_node = self.root

        fixing_node.color = Color.Black

    def _transplant(self, deleting_node: Node,
                    replacing_node: Union[Node, LeafNode]) -> None:
        if isinstance(deleting_node.parent, LeafNode):
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        replacing_node.parent = deleting_node.parent

    def _inorder_traverse(self, node: Union[Node, LeafNode]) -> traversal.Pairs:
        if isinstance(node, Node):
            yield from self._inorder_traverse(node.left)
            yield (node.key, node.data)
            yield from self._inorder_traverse(node.right)

    def _preorder_traverse(self, node: Union[Node, LeafNode]) -> traversal.Pairs:
        if isinstance(node, Node):
            yield (node.key, node.data)
            yield from self._preorder_traverse(node.left)
            yield from self._preorder_traverse(node.right)

    def _postorder_traverse(self, node: Union[Node, LeafNode]) -> traversal.Pairs:
        if isinstance(node, Node):
            yield from self._postorder_traverse(node.left)
            yield from self._postorder_traverse(node.right)
            yield (node.key, node.data)
