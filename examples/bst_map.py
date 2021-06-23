"""The module demonstrates using a Binary Search Tree to implement Map."""

from typing import Any, Optional

from forest.binary_trees import binary_search_tree
from forest.binary_trees import traversal


class Map:
    """Key-value Map implemented by a Binary Search Tree."""

    def __init__(self) -> None:
        self._bst = binary_search_tree.BinarySearchTree()

    def __setitem__(self, key: Any, value: Any) -> None:
        """Insert (key, value) item into the map."""
        self._bst.insert(key=key, data=value)

    def __getitem__(self, key: Any) -> Optional[Any]:
        """Get the data by the given key."""
        node = self._bst.search(key=key)
        if node:
            return node.data
        return None

    def __delitem__(self, key: Any) -> None:
        """Remove a (key, value) pair from the map."""
        self._bst.delete(key=key)

    def __iter__(self) -> traversal.Pairs:
        """Iterate the data in the map."""
        return traversal.inorder_traverse(tree=self._bst)

    @property
    def empty(self) -> bool:
        """Return `True` if the map is empty; `False` otherwise."""
        return self._bst.empty


if __name__ == "__main__":

    # Initialize the Map instance.
    contacts = Map()

    # Add some items.
    contacts["Mark"] = "mark@email.com"
    contacts["John"] = "john@email.com"
    contacts["Luke"] = "luke@email.com"

    # Retrieve an email
    print(contacts["Mark"])

    # Delete one item.
    del contacts["John"]

    # Check the deleted item.
    print(contacts["John"])  # This will print None

    # Iterate the items.
    for contact in contacts:
        print(contact)
