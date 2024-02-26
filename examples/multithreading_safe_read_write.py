"""Example to show atomic trees are thread-safe in read-write contention situation."""

import threading
import sys

from typing import Any

from forest.binary_trees import atomic_trees


# Use a very small thread switch interval to increase the chance that
# we can reveal the multithreading issue easily.
sys.setswitchinterval(0.0000001)


flag = False


def delete_data(tree: atomic_trees.AVLTree, data: list) -> None:
    """Delete data from a tree."""
    for key in data:
        tree.delete(key=key)


def find_node(tree: atomic_trees.AVLTree, key: Any) -> None:
    """Search a specific node."""
    global flag
    while flag:
        if not tree.search(key):
            print(f"  Fail to find node: {key}")


def multithreading_simulator(tree: atomic_trees.AVLTree, tree_size: int) -> None:
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
    print(f"Check if the node {query_node_key} exist?")
    if tree.search(key=query_node_key):
        print(f"{query_node_key} exists")


if __name__ == "__main__":
    print("Build an AVL Tree")
    tree = atomic_trees.AVLTree()
    tree_size = 200
    for key in range(tree_size):
        tree.insert(key=key, data=str(key))
    print("Multithreading Read/Write Test")
    multithreading_simulator(tree=tree, tree_size=tree_size)
