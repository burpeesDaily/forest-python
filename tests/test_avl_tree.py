"""Unit tests for the AVL tree module."""

import pytest

from forest import tree_exceptions

from forest.binary_trees import avl_tree
from forest.binary_trees import traversal


def test_simple_case(basic_tree):
    """Test the basic operation of an AVL tree."""
    tree = avl_tree.AVLTree()

    assert tree.empty

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert tree.empty is False

    with pytest.raises(tree_exceptions.DuplicateKeyError):
        tree.insert(key=23, data="23")

    assert tree.get_leftmost(tree.root).key == 1
    assert tree.get_leftmost(tree.root).data == "1"
    assert tree.get_rightmost(tree.root).key == 34
    assert tree.get_rightmost(tree.root).data == "34"
    assert tree.search(24).key == 24
    assert tree.search(24).data == "24"

    tree.delete(key=15)
    assert tree.search(key=15) is None


def test_traversal(basic_tree):
    """Test the traversal on an AVL tree."""
    tree = avl_tree.AVLTree()
    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)
    with pytest.raises(tree_exceptions.DuplicateKeyError):
        tree.insert(key=23, data="23")

    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (15, "15"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    assert [item for item in traversal.inorder_traverse(tree, False)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (15, "15"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    assert [item for item in traversal.preorder_traverse(tree)] == [
        (23, "23"),
        (11, "11"),
        (4, "4"),
        (1, "1"),
        (7, "7"),
        (20, "20"),
        (15, "15"),
        (22, "22"),
        (30, "30"),
        (24, "24"),
        (34, "34"),
    ]

    assert [item for item in traversal.preorder_traverse(tree, False)] == [
        (23, "23"),
        (11, "11"),
        (4, "4"),
        (1, "1"),
        (7, "7"),
        (20, "20"),
        (15, "15"),
        (22, "22"),
        (30, "30"),
        (24, "24"),
        (34, "34"),
    ]

    assert [item for item in traversal.postorder_traverse(tree)] == [
        (1, "1"),
        (7, "7"),
        (4, "4"),
        (15, "15"),
        (22, "22"),
        (20, "20"),
        (11, "11"),
        (24, "24"),
        (34, "34"),
        (30, "30"),
        (23, "23"),
    ]

    assert [item for item in traversal.postorder_traverse(tree, False)] == [
        (1, "1"),
        (7, "7"),
        (4, "4"),
        (15, "15"),
        (22, "22"),
        (20, "20"),
        (11, "11"),
        (24, "24"),
        (34, "34"),
        (30, "30"),
        (23, "23"),
    ]

    assert [item for item in traversal.reverse_inorder_traverse(tree)] == [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (23, "23"),
        (22, "22"),
        (20, "20"),
        (15, "15"),
        (11, "11"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
    ]

    assert [item for item in traversal.reverse_inorder_traverse(tree, False)] == [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (23, "23"),
        (22, "22"),
        (20, "20"),
        (15, "15"),
        (11, "11"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
    ]


def test_deletion(basic_tree):
    """Test the deletion of an AVL tree."""
    tree = avl_tree.AVLTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    # No child
    tree.delete(15)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # One right child
    tree.delete(20)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]
    # One left child
    tree.insert(key=17, data="17")
    tree.delete(22)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (17, "17"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # Two children
    tree.delete(11)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (17, "17"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]


def test_delete_two_children_1():
    """Test the two children deletion."""
    tree = avl_tree.AVLTree()

    test_tree = [
        (37, "37"),
        (29, "29"),
        (55, "55"),
        (17, "17"),
        (41, "41"),
        (63, "63"),
        (57, "57"),
    ]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(key=37)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (17, "17"),
        (29, "29"),
        (41, "41"),
        (55, "55"),
        (57, "57"),
        (63, "63"),
    ]

    assert [item for item in traversal.preorder_traverse(tree)] == [
        (41, "41"),
        (29, "29"),
        (17, "17"),
        (57, "57"),
        (55, "55"),
        (63, "63"),
    ]


def test_delete_two_children_2():
    """Test the two children deletion."""
    tree = avl_tree.AVLTree()

    test_tree = [
        (37, "37"),
        (29, "29"),
        (55, "55"),
        (17, "17"),
        (35, "35"),
        (63, "63"),
        (31, "31"),
    ]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(key=37)
    assert [item for item in traversal.inorder_traverse(tree)] == [
        (17, "17"),
        (29, "29"),
        (31, "31"),
        (35, "35"),
        (55, "55"),
        (63, "63"),
    ]

    assert [item for item in traversal.preorder_traverse(tree)] == [
        (35, "35"),
        (29, "29"),
        (17, "17"),
        (31, "31"),
        (55, "55"),
        (63, "63"),
    ]
