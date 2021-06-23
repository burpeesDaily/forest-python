"""The module compare the performance of BST, AVL Tree, and Red-Black Tree."""

import random

from forest import metrics
from forest.binary_trees import avl_tree
from forest.binary_trees import binary_search_tree
from forest.binary_trees import red_black_tree


insert_data = random.sample(range(1, 2000), 1000)
delete_data = random.sample(insert_data, 1000)

registry = metrics.MetricsRegistry()
bstree = binary_search_tree.BinarySearchTree(registry=registry)
avltree = avl_tree.AVLTree(registry=registry)
rbtree = red_black_tree.RBTree(registry=registry)

for key in insert_data:
    bstree.insert(key=key, data=str(key))
    avltree.insert(key=key, data=str(key))
    rbtree.insert(key=key, data=str(key))

for key in delete_data:
    bstree.delete(key=key)
    avltree.delete(key=key)
    rbtree.delete(key=key)

print("Binary Search Tree:")
bst_report = registry.get_metric(name="bst.height").report()
print(f"  Height:   {bst_report}")

print("AVL Tree:")
avlt_rotation_count = registry.get_metric(name="avlt.rotate").count
print(f"  Rotation: {avlt_rotation_count}")
avlt_report = registry.get_metric(name="avlt.height").report()
print(f"  Height:   {avlt_report}")

print("Red-Black Tree")
rbt_rotation_count = registry.get_metric(name="rbt.rotate").count
print(f"  Rotation: {rbt_rotation_count}")
rbt_repot = registry.get_metric(name="rbt.height").report()
print(f"  Height:   {rbt_repot}")
