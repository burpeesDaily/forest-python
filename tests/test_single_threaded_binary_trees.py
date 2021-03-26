"""Unit tests for the single threaded binary search tree module."""

from forest.binary_trees import single_threaded_binary_trees


def test_simple_right_threaded_case(basic_tree):
    """Test the basic opeartions of a right threaded binary search tree."""
    tree = single_threaded_binary_trees.RightThreadedBinaryTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert [
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
    ] == [item for item in tree.inorder_traverse()]

    assert [
        (23, "23"),
        (4, "4"),
        (1, "1"),
        (11, "11"),
        (7, "7"),
        (20, "20"),
        (15, "15"),
        (22, "22"),
        (30, "30"),
        (24, "24"),
        (34, "34"),
    ] == [item for item in tree.preorder_traverse()]

    assert tree.get_leftmost(node=tree.root).key == 1
    assert tree.get_rightmost(node=tree.root).key == 34
    assert tree.search(key=24).data == "24"

    tree.delete(key=34)
    assert tree.search(key=34) is None

    tree.delete(key=15)
    tree.delete(key=22)
    tree.delete(key=7)
    tree.delete(key=20)

    assert tree.search(key=15) is None

    assert [(1, "1"), (4, "4"), (11, "11"), (23, "23"), (24, "24"), (30, "30")] == [
        item for item in tree.inorder_traverse()
    ]


def test_deletion_right_threaded_case(basic_tree):
    """Test the deletion of a right threaded binary search tree."""
    tree = single_threaded_binary_trees.RightThreadedBinaryTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    # No child
    tree.delete(15)
    assert [
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
    ] == [item for item in tree.inorder_traverse()]

    # One right child
    tree.delete(20)
    assert [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (22, "22"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ] == [item for item in tree.inorder_traverse()]

    # One left child
    tree.insert(key=17, data="17")
    tree.delete(22)
    assert [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (17, "17"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ] == [item for item in tree.inorder_traverse()]

    # Two children
    tree.delete(11)
    assert [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (17, "17"),
        (23, "23"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ] == [item for item in tree.inorder_traverse()]

    # Delete the root
    tree.delete(23)
    assert [
        (1, "1"),
        (4, "4"),
        (7, "7"),
        (17, "17"),
        (24, "24"),
        (30, "30"),
        (34, "34"),
    ] == [item for item in tree.inorder_traverse()]


def test_simple_left_threaded_case(basic_tree):
    """Test the basic opeartions of a left threaded binary search tree."""
    tree = single_threaded_binary_trees.LeftThreadedBinaryTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    assert [
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
    ] == [item for item in tree.reverse_inorder_traverse()]

    assert tree.get_leftmost(node=tree.root).key == 1
    assert tree.get_rightmost(node=tree.root).key == 34
    assert tree.search(key=24).data == "24"

    tree.delete(key=15)
    tree.delete(key=22)
    tree.delete(key=7)
    tree.delete(key=20)

    assert tree.search(key=15) is None

    assert [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (23, "23"),
        (11, "11"),
        (4, "4"),
        (1, "1"),
    ] == [item for item in tree.reverse_inorder_traverse()]


def test_deletion_left_threaded_case(basic_tree):
    """Test the deletion of a left threaded binary search tree."""
    tree = single_threaded_binary_trees.LeftThreadedBinaryTree()

    # 23, 4, 30, 11, 7, 34, 20, 24, 22, 15, 1
    for key, data in basic_tree:
        tree.insert(key=key, data=data)

    # No child
    tree.delete(15)
    assert [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (23, "23"),
        (22, "22"),
        (20, "20"),
        (11, "11"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
    ] == [item for item in tree.reverse_inorder_traverse()]

    # One right child
    tree.delete(20)
    assert [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (23, "23"),
        (22, "22"),
        (11, "11"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
    ] == [item for item in tree.reverse_inorder_traverse()]

    # One left child
    tree.insert(key=17, data="17")
    tree.delete(22)
    assert [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (23, "23"),
        (17, "17"),
        (11, "11"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
    ] == [item for item in tree.reverse_inorder_traverse()]

    # Two children
    tree.delete(11)
    assert [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (23, "23"),
        (17, "17"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
    ] == [item for item in tree.reverse_inorder_traverse()]

    # Delete the root
    tree.delete(23)
    assert [
        (34, "34"),
        (30, "30"),
        (24, "24"),
        (17, "17"),
        (7, "7"),
        (4, "4"),
        (1, "1"),
    ] == [item for item in tree.reverse_inorder_traverse()]
