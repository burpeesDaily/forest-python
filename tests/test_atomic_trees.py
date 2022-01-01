"""Unit tests for atomic trees."""
import sys
import threading

from typing import List, Union

from forest.binary_trees import atomic_trees
from forest.binary_trees import traversal


sys.setswitchinterval(0.0000001)


TreeType = Union[
    atomic_trees.AVLTree,
    atomic_trees.BinarySearchTree,
    atomic_trees.DoubleThreadedBinaryTree,
    atomic_trees.LeftThreadedBinaryTree,
    atomic_trees.RBTree,
    atomic_trees.RightThreadedBinaryTree,
]


def insert_data(tree: TreeType, data: List) -> None:
    """Insert data into a tree."""
    for key in data:
        tree.insert(key=key, data=str(key))


def multithreading_simulator(tree: TreeType) -> bool:
    """Use five threads to insert data into a tree with non-duplicate data."""
    thread1 = threading.Thread(
        target=insert_data, args=(tree, [item for item in range(100)])
    )
    thread2 = threading.Thread(
        target=insert_data, args=(tree, [item for item in range(100, 200)])
    )
    thread3 = threading.Thread(
        target=insert_data, args=(tree, [item for item in range(200, 300)])
    )
    thread4 = threading.Thread(
        target=insert_data, args=(tree, [item for item in range(300, 400)])
    )
    thread5 = threading.Thread(
        target=insert_data, args=(tree, [item for item in range(400, 500)])
    )

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

    if isinstance(tree, atomic_trees.LeftThreadedBinaryTree):
        result = [item for item in tree.reverse_inorder_traverse()]
        for index in range(len(result)):
            if index > 0:
                if result[index] > result[index - 1]:
                    return False
    else:
        if isinstance(tree, atomic_trees.AVLTree) or isinstance(
            tree, atomic_trees.BinarySearchTree
        ):
            result = [item for item in traversal.inorder_traverse(tree=tree)]
        else:
            result = [item for item in tree.inorder_traverse()]

        for index in range(len(result)):
            if index > 0:
                if result[index] < result[index - 1]:
                    return False

    if len(result) != 500:
        return False

    return True


def test_atomic_avl_tree():
    """Test if atomic AVL tree is thread-safe."""
    tree = atomic_trees.AVLTree()
    assert multithreading_simulator(tree=tree) is True


def test_atomic_binary_search_tree():
    """Test if atomic binary search tree is thread-safe."""
    tree = atomic_trees.BinarySearchTree()
    assert multithreading_simulator(tree=tree) is True


def test_atomic_double_threaded_tree():
    """Test if atomic double threaded tree is thread-safe."""
    tree = atomic_trees.DoubleThreadedBinaryTree()
    assert multithreading_simulator(tree=tree) is True


def test_atomic_red_black_tree():
    """Test if atomic red-black tree is thread-safe."""
    tree = atomic_trees.RBTree()
    assert multithreading_simulator(tree=tree) is True


def test_atomic_left_threaded_tree():
    """Test if atomic left threaded tree is thread-safe."""
    tree = atomic_trees.LeftThreadedBinaryTree()
    assert multithreading_simulator(tree=tree)


def test_atomic_right_threaded_tree():
    """Test if atomic right threaded tree is thread-safe."""
    tree = atomic_trees.RightThreadedBinaryTree()
    assert multithreading_simulator(tree=tree)
