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

print(registry.get_metric(key="avlt.rotate").count)
print(registry.get_metric(key="avlt.height").report())
print(registry.get_metric(key="rbt.rotate").count)
print(registry.get_metric(key="rbt.height").report())


for key in delete_data:
    avltree.delete(key=key)
    rbtree.delete(key=key)
print(registry.get_metric(key="avlt.rotate").count)
print(registry.get_metric(key="avlt.height").report())
print(registry.get_metric(key="rbt.rotate").count)
print(registry.get_metric(key="rbt.height").report())
