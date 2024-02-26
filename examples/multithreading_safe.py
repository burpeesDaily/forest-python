"""Example to show atomic trees are thread-safe in write contention situation."""

import threading
import sys

from typing import Union

from forest.binary_trees import atomic_trees
from forest.binary_trees import traversal


TreeType = Union[
    atomic_trees.AVLTree,
    atomic_trees.BinarySearchTree,
    atomic_trees.DoubleThreadedBinaryTree,
    atomic_trees.RBTree,
]

sys.setswitchinterval(0.0000001)


def insert_data(tree: TreeType, data: list) -> None:
    """Insert data into a tree."""
    for key in data:
        tree.insert(key=key, data=str(key))


def multithreading_simulator(tree: TreeType) -> None:
    """Use five threads to insert data into a tree with non-duplicate data."""
    try:
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

        if isinstance(tree, atomic_trees.AVLTree) or isinstance(
            tree, atomic_trees.BinarySearchTree
        ):
            result = [item for item in traversal.inorder_traverse(tree=tree)]
        else:
            result = [item for item in tree.inorder_traverse()]

        incorrect_node_list = list()
        for index in range(len(result)):
            if index > 0:
                if result[index] < result[index - 1]:
                    incorrect_node_list.append(
                        f"{result[index - 1]} -> {result[index]}"
                    )

        if len(result) != 500 or len(incorrect_node_list) > 0:
            print(f"  total_nodes: {len(result)}")
            print(f"  incorrect_order: {incorrect_node_list}")
    except:  # noqa: 1722
        print("  Tree built incorrectly.")


if __name__ == "__main__":
    print("Atomic AVL Tree:")
    avlt = atomic_trees.AVLTree()
    multithreading_simulator(tree=avlt)

    print("Atomic Binary Search Tree:")
    bst = atomic_trees.BinarySearchTree()
    multithreading_simulator(tree=bst)

    print("Atomic Double Threaded Binary Search Tree:")
    double_threaded = atomic_trees.DoubleThreadedBinaryTree()
    multithreading_simulator(tree=double_threaded)

    print("Atomic Red-Black Tree:")
    rbt = atomic_trees.RBTree()
    multithreading_simulator(tree=rbt)
