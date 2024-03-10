import unittest
from pyinmem import MemStore, Cursor


class TestMemStore(unittest.TestCase):
    def setUp(self):
        self.store = MemStore()

    def test_set_and_get(self):
        self.store.set('key', ['value', None])
        self.assertEqual(self.store.get('key'), ['value', None])

    def test_unset(self):
        self.store.set('key', ['value', None])
        self.store.unset('key')
        self.assertIsNone(self.store.get('key'))

    def test_get_all(self):
        self.store.set('key1', ['value1', None])
        self.store.set('key2', ['value2', None])
        self.assertEqual(self.store.get_all(), {'key1': ['value1', None], 'key2': ['value2', None]})


class TestCursor(unittest.TestCase):
    def setUp(self):
        self.store = MemStore()
        self.cursor = Cursor(self.store)

    def test_set_and_get(self):
        self.cursor.set('key', 'value')
        self.assertEqual(self.cursor.get('key'), 'value')

    def test_delete(self):
        self.cursor.set('key', 'value')
        self.cursor.delete('key')
        self.assertIsNone(self.cursor.get('key'))

    def test_set_and_get_expiry(self):
        self.cursor.set('key', 'value')
        self.cursor.set_expiry('key', 10)
        self.assertGreater(self.cursor.get_expiry('key'), 0)

    def test_commit(self):
        self.cursor.set('key', 'value')
        self.cursor.commit()
        self.assertEqual(self.store.get('key'), ['value', None])

    def test_rollback(self):
        self.cursor.set('key', 'value')
        self.cursor.rollback()
        self.assertIsNone(self.cursor.get('key'))


if __name__ == '__main__':
    unittest.main()
