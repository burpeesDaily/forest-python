import random

from forest import metrics
from forest.binary_trees import avl_tree
from forest.binary_trees import red_black_tree


def list_diff(my_list1, my_list2):
    out = [item for item in my_list1 if not item in my_list2]
    return out


insert_data = random.sample(range(1, 2000), 1000)
delete_data = random.sample(insert_data, 500)
remining_data = list_diff(insert_data, delete_data)
remining_data.sort()

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


output = [item for item, _ in rbtree.inorder_traverse()]

print(len(output))
print(len(remining_data))
for index in range(len(output)):
    print(output[index], remining_data[index])


if output == remining_data:
    print(True)
