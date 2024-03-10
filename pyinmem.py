import json
import threading
import time
from collections import defaultdict
from typing import Dict, List, Union, Any


class MemStore:
    """
    A class used to represent an in-memory store.

    Attributes
    ----------
    __data : dict
        a dictionary to store the data
    __locks : defaultdict(threading.Lock)
        a dictionary to store the locks for each key
    """

    def __init__(self) -> None:
        """Initialize the MemStore with an empty data dictionary, locks dictionary and a cleanup thread."""
        self.__data: Dict[str, List[Union[Any, int]]] = {}
        self.__locks: Dict[str, threading.Lock] = defaultdict(threading.Lock)
        self.__cleanup_thread: threading.Thread = threading.Thread(target=self.__cleanup_expired_keys, daemon=True)
        self.__cleanup_thread.start()
        self.restore_data()

    def get_lock(self, key: str) -> threading.Lock:
        """Get the lock for a given key."""
        return self.__locks[key]

    def get(self, key: str) -> Union[List[Union[str, int]], None]:
        """Get the value for a given key."""
        return self.__data.get(key)

    def get_all(self) -> Dict[str, List[Union[Any, int]]]:
        """Get all the data in the store."""
        return self.__data

    def set(self, key: str, value: List[Union[Any, int]]) -> bool:
        """Set the value for a given key."""
        with self.get_lock(key):
            self.__data[key] = value
        return True

    def unset(self, key: str) -> bool:
        """Unset the value for a given key."""
        with self.get_lock(key):
            if key in self.__data:
                del self.__data[key]
            return True

    def __cleanup_expired_keys(self) -> None:
        """Cleanup expired keys in a separate thread."""
        while True:
            keys = list(self.__data.keys())
            for key in keys:
                with self.get_lock(key):
                    if self.__data.get(key) and self.__data[key][1] and self.__data[key][1] < time.time():
                        del self.__data[key]
            time.sleep(1)

    def make_backup(self) -> None:
        """Make a backup of the data to a JSON file."""
        with open('backup.json', 'w') as f:
            json.dump(self.__data, f)

    def restore_data(self) -> None:
        """Restore the data from the JSON file."""
        try:
            with open('backup.json', 'r') as f:
                self.__data = json.load(f)
        except FileNotFoundError:
            pass


class Cursor:
    """
    A class used to represent a cursor for the in-memory store.

    Attributes
    ----------
    DELETED : object
        a unique object to represent a deleted key
    database : MemStore
        The in-memory database this cursor will interact with.
    data : dict
        a dictionary to store the data for the cursor
    """

    DELETED = object()

    def __init__(self, database: MemStore) -> None:
        """Initialize the Cursor with a given store and an empty data dictionary."""
        self.database: MemStore = database
        self.data: Dict[str, List[Union[Any, int, object]]] = {}

    def set(self, key: str, value: Any) -> bool:
        """Set the value for a given key."""
        with self.database.get_lock(key):
            self.data[key] = [value, None]
        return True

    def get(self, key: str) -> Union[Any, None]:
        """Get the value for a given key."""
        with self.database.get_lock(key):
            if key in self.data and self.data[key][0] != self.DELETED:
                return self.data[key][0]
            elif self.database.get(key):
                return self.database.get(key)[0]
            return None

    def delete(self, key: str) -> bool:
        """Delete the value for a given key."""
        with self.database.get_lock(key):
            self.data[key] = [self.DELETED]
            return True

    def set_expiry(self, key: str, seconds: float) -> bool:
        """Set the expiry time for a given key."""
        with self.database.get_lock(key):
            value = self.data.get(key) if key in self.data else self.database.get(key)
            self.data[key] = [value, time.time() + seconds]
            return True

    def get_expiry(self, key: str) -> Union[int, None]:
        """Get the expiry time for a given key."""
        with self.database.get_lock(key):
            value = self.data.get(key) if key in self.data else self.database.get(key)
            if value:
                return value[1]
            return None

    def commit(self) -> None:
        """Commit the changes in the cursor to the store."""
        items = list(self.data.items())
        for key, value in items:
            if value[0] == self.DELETED:
                self.database.unset(key)
            else:
                self.database.set(key, value)
        self.data = {}

    def rollback(self) -> None:
        """Rollback the changes in the cursor."""
        self.data = {}
