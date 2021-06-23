import random

from forest import metrics
from forest.binary_trees import avl_tree
from forest.binary_trees import red_black_tree


sample_data = random.sample(range(1, 3000), 2000)
insert_data = [("insert", item) for item in sample_data]

sample_data = random.sample(range(1, 3000), 1000)
delete_data = [("delete", item) for item in sample_data]

test_data = random.sample(
    (insert_data + delete_data), len(insert_data) + len(delete_data)
)

registry = metrics.MetricsRegistry()
avltree = avl_tree.AVLTree(registry=registry)
rbtree = red_black_tree.RBTree(registry=registry)

for operation, key in test_data:
    if operation == "insert":
        avltree.insert(key=key, data=str(key))
        rbtree.insert(key=key, data=str(key))
    if operation == "delete":
        avltree.delete(key=key)
        rbtree.delete(key=key)

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
