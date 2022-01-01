"""Unit tests for the red black tree module."""

import random
import pytest

from forest import metrics
from forest import tree_exceptions
from forest.binary_trees import red_black_tree


def test_simple_case(basic_tree):
    """Test the basic operations of a red black tree."""
    tree = red_black_tree.RBTree()
    assert tree.empty

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert tree.empty is False

    with pytest.raises(tree_exceptions.DuplicateKeyError):
        tree.insert(key=23, data="23")

    assert tree.get_height(node=tree.root) == 3
    assert tree.get_leftmost(tree.root).key == 1
    assert tree.get_leftmost(tree.root).data == "1"
    assert tree.get_rightmost(tree.root).key == 34
    assert tree.get_rightmost(tree.root).data == "34"
    assert tree.search(24).key == 24
    assert tree.search(24).data == "24"
    node = tree.search(7)
    assert tree.get_successor(node).key == 11
    assert tree.get_predecessor(node).key == 4
    node = tree.search(15)
    assert tree.get_successor(node).key == 20
    node = tree.search(22)
    assert tree.get_predecessor(node).key == 20

    tree.delete(15)

    assert tree.search(15) is None


def test_deletion(basic_tree):
    """Test the deletion of a red black tree."""
    tree = red_black_tree.RBTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    # No child
    tree.delete(15)
    assert [item for item in tree.inorder_traverse()] == [
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
    tree.delete(7)
    assert [item for item in tree.inorder_traverse()] == [
        (1, "1"),
        (4, "4"),
        (11, "11"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # One left child
    tree.insert(key=9, data="9")
    tree.delete(11)
    assert [item for item in tree.inorder_traverse()] == [
        (1, "1"),
        (4, "4"),
        (9, "9"),
        (20, "20"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]

    # Two children
    tree.delete(23)
    assert [item for item in tree.inorder_traverse()] == [
        (1, "1"),
        (4, "4"),
        (9, "9"),
        (20, "20"),
        (22, "22"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ]


def test_deletion_no_child():
    """Test the deletion of a red black tree."""
    tree = red_black_tree.RBTree()

    test_tree = [(23, "23"), (4, "4"), (30, "30"), (11, "11")]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(4)
    assert [item for item in tree.inorder_traverse()] == [
        (11, "11"),
        (23, "23"),
        (30, "30"),
    ]


def test_deletion_one_child():
    """Test the deletion of a red black tree."""
    tree = red_black_tree.RBTree()

    # 23, 4, 30, 11, 7, 34, 9
    test_tree = [
        (23, "23"),
        (4, "4"),
        (30, "30"),
        (11, "11"),
        (7, "7"),
        (34, "34"),
        (9, "9"),
    ]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(11)
    assert [item for item in tree.inorder_traverse()] == [
        (4, "4"),
        (7, "7"),
        (9, "9"),
        (23, "23"),
        (30, "30"),
        (34, "34"),
    ]


def test_deletion_two_children():
    """Test the deletion of a red black tree."""
    tree = red_black_tree.RBTree()

    test_tree = [
        (23, "23"),
        (4, "4"),
        (30, "30"),
        (11, "11"),
        (7, "7"),
        (34, "34"),
        (9, "9"),
        (27, "27"),
    ]

    for key, data in test_tree:
        tree.insert(key=key, data=data)

    tree.delete(23)
    assert [item for item in tree.inorder_traverse()] == [
        (4, "4"),
        (7, "7"),
        (9, "9"),
        (11, "11"),
        (27, "27"),
        (30, "30"),
        (34, "34"),
    ]


def test_red_black_tree_traversal(basic_tree):
    """Test red black tree traversal."""
    tree = red_black_tree.RBTree()

    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert [item for item in tree.inorder_traverse()] == [
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

    assert [item for item in tree.preorder_traverse()] == [
        (20, "20"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
        (11, "11"),
        (15, "15"),
        (23, "23"),
        (22, "22"),
        (30, "30"),
        (24, "24"),
        (34, "34"),
    ]

    assert [item for item in tree.postorder_traverse()] == [
        (1, "1"),
        (4, "4"),
        (15, "15"),
        (11, "11"),
        (7, "7"),
        (22, "22"),
        (24, "24"),
        (34, "34"),
        (30, "30"),
        (23, "23"),
        (20, "20"),
    ]


def test_random_insert_delete():
    """Test random insert and delete."""
    for _ in range(0, 10):
        insert_data = random.sample(range(1, 2000), 1000)
        delete_data = random.sample(insert_data, 500)

        remaining_data = [item for item in insert_data if item not in delete_data]
        remaining_data.sort()

        tree = red_black_tree.RBTree()
        for key in insert_data:
            tree.insert(key=key, data=str(key))

        for key in delete_data:
            tree.delete(key=key)

        result = [item for item, _ in tree.inorder_traverse()]
        assert result == remaining_data


def test_metrics(basic_tree):
    """Test red-black tree with metrics enabled."""
    registry = metrics.MetricRegistry()
    tree = red_black_tree.RBTree(registry=registry)

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert registry.get_metric(name="rbt.rotate").count
    assert registry.get_metric(name="rbt.height").report()


def test_empty():
    """Test red-black becomes empty."""
    tree = red_black_tree.RBTree()

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
