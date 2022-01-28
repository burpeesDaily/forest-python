"""Demonstrate the trees are not thread-safe in read-write contention situation."""
import threading
import sys

from typing import Any, List

from forest.binary_trees import avl_tree


# Use a very small thread switch interval to increase the chance that
# we can reveal the multithreading issue easily.
sys.setswitchinterval(0.0000001)


flag = False  # Flag to determine if the read thread stops or continues.


def delete_data(tree: avl_tree.AVLTree, data: List) -> None:
    """Delete data from a tree."""
    for key in data:
        tree.delete(key=key)


def find_node(tree: avl_tree.AVLTree, key: Any) -> None:
    """Search a specific node."""
    while flag:
        if not tree.search(key):
            print(f"  Fail to find node: {key}")


def multithreading_simulator(tree: avl_tree.AVLTree, tree_size: int) -> None:
    """Use one thread to delete data and one thread to query at the same time."""
    global flag
    flag = True
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
    print(f"Check if node {query_node_key} exist?")
    if tree.search(key=query_node_key):
        print(f"{query_node_key} exists")


if __name__ == "__main__":
    print("Build an AVL Tree")
    tree = avl_tree.AVLTree()
    tree_size = 200
    for key in range(tree_size):
        tree.insert(key=key, data=str(key))
    print("Multithreading Read/Write Test")
    multithreading_simulator(tree=tree, tree_size=tree_size)
