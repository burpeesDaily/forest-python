"""Unit tests for atomic trees."""
import sys
import threading

from typing import Any, Union

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


def insert_data(tree: TreeType, data: list) -> None:
    """Insert data into a tree."""
    for key in data:
        tree.insert(key=key, data=str(key))


def delete_data(tree: TreeType, data: list) -> None:
    """Delete data from a tree."""
    for key in data:
        tree.delete(key=key)


def multithreading_simulator_write_contention(tree: TreeType) -> bool:
    """Use five threads to insert and delete with non-duplicate data."""
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

    thread1 = threading.Thread(
        target=delete_data, args=(tree, [item for item in range(100)])
    )
    thread2 = threading.Thread(
        target=delete_data, args=(tree, [item for item in range(100, 200)])
    )
    thread3 = threading.Thread(
        target=delete_data, args=(tree, [item for item in range(200, 300)])
    )
    thread4 = threading.Thread(
        target=delete_data, args=(tree, [item for item in range(300, 400)])
    )
    thread5 = threading.Thread(
        target=delete_data, args=(tree, [item for item in range(400, 500)])
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

    if not tree.empty:
        False

    return True


flag = False
if_exist = True


def find_node(tree: atomic_trees.AVLTree, key: Any) -> None:
    """Search a specific node."""
    while flag:
        if not tree.search(key):
            global if_exist
            if_exist = False


def multithreading_simulator_read_write_contention(tree: TreeType) -> bool:
    """Use one thread to delete data and one thread to query at the same time."""
    global flag
    flag = True
    global if_exist
    if_exist = True
    tree_size = 2000
    for key in range(tree_size):
        tree.insert(key=key, data=str(key))

    delete_thread = threading.Thread(
        target=delete_data, args=(tree, [item for item in range(20, tree_size)])
    )
    query_node_key = 17
    query_thread = threading.Thread(target=find_node, args=(tree, query_node_key))

    delete_thread.start()
    query_thread.start()

    delete_thread.join()
    flag = False
    query_thread.join()

    return if_exist


def test_atomic_avl_tree_write_contention():
    """Test if atomic AVL tree is thread-safe."""
    assert multithreading_simulator_write_contention(tree=atomic_trees.AVLTree())


def test_atomic_avl_tree_read_write_contention():
    """Test if atomic AVL tree is thread-safe."""
    assert multithreading_simulator_read_write_contention(tree=atomic_trees.AVLTree())


def test_atomic_binary_search_tree_write_contention():
    """Test if atomic binary search tree is thread-safe."""
    assert multithreading_simulator_write_contention(
        tree=atomic_trees.BinarySearchTree()
    )


def test_atomic_binary_search_tree_read_write_contention():
    """Test if atomic binary search tree is thread-safe."""
    assert multithreading_simulator_read_write_contention(
        tree=atomic_trees.BinarySearchTree()
    )


def test_atomic_double_threaded_tree_write_contention():
    """Test if atomic double threaded tree is thread-safe."""
    assert multithreading_simulator_write_contention(
        tree=atomic_trees.DoubleThreadedBinaryTree()
    )


def test_atomic_double_threaded_tree_read_write_contention():
    """Test if atomic double threaded tree is thread-safe."""
    assert multithreading_simulator_read_write_contention(
        tree=atomic_trees.DoubleThreadedBinaryTree()
    )


def test_atomic_red_black_tree_write_contention():
    """Test if atomic red-black tree is thread-safe."""
    assert multithreading_simulator_write_contention(tree=atomic_trees.RBTree())


def test_atomic_red_black_tree_read_write_contention():
    """Test if atomic red-black tree is thread-safe."""
    assert multithreading_simulator_read_write_contention(tree=atomic_trees.RBTree())


def test_atomic_left_threaded_tree_write_contention():
    """Test if atomic left threaded tree is thread-safe."""
    assert multithreading_simulator_write_contention(
        tree=atomic_trees.LeftThreadedBinaryTree()
    )


def test_atomic_left_threaded_tree_read_write_contention():
    """Test if atomic left threaded tree is thread-safe."""
    assert multithreading_simulator_read_write_contention(
        tree=atomic_trees.LeftThreadedBinaryTree()
    )


def test_atomic_right_threaded_tree_write_contention():
    """Test if atomic right threaded tree is thread-safe."""
    assert multithreading_simulator_write_contention(
        tree=atomic_trees.RightThreadedBinaryTree()
    )


def test_atomic_right_threaded_tree_read_write_contention():
    """Test if atomic right threaded tree is thread-safe."""
    assert multithreading_simulator_read_write_contention(
        tree=atomic_trees.RightThreadedBinaryTree()
    )
