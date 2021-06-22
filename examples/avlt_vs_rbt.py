import random

from forest import metrics
from forest.binary_trees import avl_tree
from forest.binary_trees import red_black_tree


insert_data = random.sample(range(1, 2000), 1000)
delete_data = random.sample(insert_data, 1000)

registry = metrics.MetricsRegistry()
avltree = avl_tree.AVLTree(registry=registry)
rbtree = red_black_tree.RBTree(registry=registry)

for key in insert_data:
    avltree.insert(key=key, data=str(key))
    rbtree.insert(key=key, data=str(key))

for key in delete_data:
    avltree.delete(key=key)
    rbtree.delete(key=key)

print("AVL Tree:")
avlt_rotation_count = registry.get_metric(key="avlt.rotate").count
print(f"  Rotation: {avlt_rotation_count}")
avlt_report = registry.get_metric(key="avlt.height").report()
print(f"  Height:   {avlt_report}")

print("Red-Black Tree")
rbt_rotation_count = registry.get_metric(key="rbt.rotate").count
print(f"  Rotation: {rbt_rotation_count}")
rbt_repot = registry.get_metric(key="rbt.height").report()
print(f"  Height:   {rbt_repot}")
