"""Module to measure the performance using multithreading."""
import threading
import time

from typing import List, Union
from forest.binary_trees import avl_tree
from forest.binary_trees import atomic_trees


def query_data(tree: Union[atomic_trees.AVLTree, avl_tree.AVLTree], data: List) -> None:
    """Query nodes from a tree."""
    for key in data:
        tree.search(key=key)


def multithreading_simulator(
    tree: Union[atomic_trees.AVLTree, avl_tree.AVLTree], total_nodes: int
) -> float:
    """Use two threads to query nodes with different ranges."""
    thread1 = threading.Thread(
        target=query_data, args=(tree, [item for item in range(total_nodes // 2)])
    )

    thread2 = threading.Thread(
        target=query_data,
        args=(tree, [item for item in range(total_nodes // 2, total_nodes)]),
    )

    start = time.time()
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    end = time.time()

    return end - start


if __name__ == "__main__":

    total_nodes = 200000

    original_avl_tree = avl_tree.AVLTree()

    # Single thread case
    for key in range(total_nodes):
        original_avl_tree.insert(key=key, data=str(key))

    data = [item for item in range(total_nodes)]
    start = time.time()
    query_data(tree=original_avl_tree, data=data)
    end = time.time()
    delta = end - start
    print("Single Thread Case")
    print(f"Time in seconds: {delta}")

    # Multithreads case
    delta_with_threads = multithreading_simulator(
        tree=original_avl_tree, total_nodes=total_nodes
    )
    print("Multithread Case")
    print(f"Time in seconds: {delta_with_threads}")

    # Multithread with lock case
    avl_tree_with_lock = atomic_trees.AVLTree()
    for key in range(total_nodes):
        avl_tree_with_lock.insert(key=key, data=str(key))

    delta_with_lock = multithreading_simulator(
        tree=avl_tree_with_lock, total_nodes=total_nodes
    )
    print("Multithread with Lock Case")
    print(f"Time in seconds: {delta_with_lock}")
