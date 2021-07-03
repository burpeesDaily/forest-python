"""The module compare the performance of BST, AVL Tree, and Red-Black Tree."""

import random

from forest import metrics
from forest.binary_trees import avl_tree
from forest.binary_trees import binary_search_tree
from forest.binary_trees import red_black_tree


sample_data = random.sample(range(1, 3000), 2000)
insert_data = [("insert", item) for item in sample_data]

sample_data = random.sample(range(1, 3000), 1000)
delete_data = [("delete", item) for item in sample_data]

test_data = random.sample(
    (insert_data + delete_data), len(insert_data) + len(delete_data)
)

registry = metrics.MetricRegistry()
bstree = binary_search_tree.BinarySearchTree(registry=registry)
avltree = avl_tree.AVLTree(registry=registry)
rbtree = red_black_tree.RBTree(registry=registry)

for operation, key in test_data:
    if operation == "insert":
        bstree.insert(key=key, data=str(key))
        avltree.insert(key=key, data=str(key))
        rbtree.insert(key=key, data=str(key))
    if operation == "delete":
        bstree.delete(key=key)
        avltree.delete(key=key)
        rbtree.delete(key=key)

print("Binary Search Tree:")
bst_report = registry.get_metric(name="bst.height").report()  # type: ignore
print(f"  Height:   {bst_report}")

print("AVL Tree:")
avlt_rotation_count = registry.get_metric(name="avlt.rotate").count  # type: ignore
print(f"  Rotation: {avlt_rotation_count}")
avlt_report = registry.get_metric(name="avlt.height").report()  # type: ignore
print(f"  Height:   {avlt_report}")

print("Red-Black Tree")
rbt_rotation_count = registry.get_metric(name="rbt.rotate").count  # type: ignore
print(f"  Rotation: {rbt_rotation_count}")
rbt_repot = registry.get_metric(name="rbt.height").report()  # type: ignore
print(f"  Height:   {rbt_repot}")
