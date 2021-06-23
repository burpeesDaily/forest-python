"""The module demonstrates using threaded binary trees to implement ordered index."""

from typing import Any

from forest.binary_trees import single_threaded_binary_trees
from forest.binary_trees import traversal


class MyDatabase:
    """Example using threaded binary trees to build index."""

    def __init__(self) -> None:
        self._left_bst = single_threaded_binary_trees.LeftThreadedBinaryTree()
        self._right_bst = single_threaded_binary_trees.RightThreadedBinaryTree()

    def _persist(self, payload: Any) -> str:
        """Fake function pretent storing data to file system.

        Returns
        -------
        str
            Path to the payload.
        """
        return f"path_to_{payload}"

    def insert_data(self, key: Any, payload: Any) -> None:
        """Insert data.

        Parameters
        ----------
        key: Any
            Unique key for the payload
        payload: Any
            Any data
        """
        path = self._persist(payload=payload)
        self._left_bst.insert(key=key, data=path)
        self._right_bst.insert(key=key, data=path)

    def dump(self, ascending: bool = True) -> traversal.Pairs:
        """Dump the data.

        Parameters
        ----------
        ascending: bool
            The order of data.

        Yields
        ------
        `Pairs`
            The next (key, data) pair.
        """
        if ascending:
            return self._right_bst.inorder_traverse()
        else:
            return self._left_bst.reverse_inorder_traverse()


if __name__ == "__main__":

    # Initialize the database.
    my_database = MyDatabase()

    # Add some items.
    my_database.insert_data("Adam", "adam_data")
    my_database.insert_data("Bob", "bob_data")
    my_database.insert_data("Peter", "peter_data")
    my_database.insert_data("David", "david_data")

    # Dump the items in ascending order.
    print("Ascending...")
    for contact in my_database.dump():
        print(contact)

    print("\nDescending...")
    # Dump the data in decending order.
    for contact in my_database.dump(ascending=False):
        print(contact)
