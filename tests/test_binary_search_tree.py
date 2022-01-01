"""Unit tests for the binary search tree module."""

import pytest

from forest import metrics
from forest import tree_exceptions
from forest.binary_trees import binary_search_tree


def test_simple_case(basic_tree: list) -> None:
    """Test the basic opeartions of a binary search tree."""
    tree = binary_search_tree.BinarySearchTree()

    assert tree.empty

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert tree.empty is False

    with pytest.raises(tree_exceptions.DuplicateKeyError):
        tree.insert(key=23, data="23")

    assert tree.get_leftmost(node=tree.root).key == 1
    assert tree.get_leftmost(node=tree.root).data == "1"
    assert tree.get_rightmost(node=tree.root).key == 34
    assert tree.get_rightmost(node=tree.root).data == "34"
    assert tree.search(key=24).data == "24"
    assert tree.get_height(node=tree.root) == 4
    assert tree.get_predecessor(node=tree.root).key == 22
    temp = tree.search(key=24)
    assert tree.get_predecessor(node=temp).key == 23
    assert tree.get_successor(node=tree.root).key == 24
    temp = tree.search(key=22)
    assert tree.get_successor(node=temp).key == 23

    tree.delete(key=22)
    tree.delete(key=20)
    tree.delete(key=11)

    assert tree.search(key=22) is None


def test_metrics(basic_tree):
    """Test binary search tree with metrics enabled."""
    registry = metrics.MetricRegistry()
    tree = binary_search_tree.BinarySearchTree(registry=registry)

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert registry.get_metric(name="bst.height").report()


def test_empty():
    """Test a tree becomes empty."""
    tree = binary_search_tree.BinarySearchTree()

    for key in range(10):
        tree.insert(key=key, data=str(key))

    for key in range(10):
        tree.delete(key=key)

    assert tree.empty

    for key in reversed(range(10)):
        tree.insert(key=key, data=str(key))

    for key in reversed(range(10)):
        tree.delete(key=key)

    assert tree.empty
