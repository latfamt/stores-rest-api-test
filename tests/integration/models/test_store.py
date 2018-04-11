"""
What to test:
-1- When we create a new store we want to make sure that the items property
    items = db.relationship('ItemModel', lazy='dynamic') is empty
-2- json method
-3- saving and writing in database works well
-4- when you add an item to the database under the store then you get an extra item on the store object
"""
from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')
        self.assertListEqual(store.items.all(), [], "The store's items length isn't 0 even though no items were added.")

    def test_crud(self):  # the writing and saving into a database
        with self.app_context():
            store = StoreModel('test')  # новый объект StoreModel

            self.assertIsNone(StoreModel.find_by_name('test'),
                              f"Found a store with name {store.name}, but expected not to")  # проверяем отсутствие в бд

            store.save_to_db()  # добавляем в бд

            self.assertIsNotNone(StoreModel.find_by_name('test'),
                                 f"Not found a store with name {store.name}, but expected to")  # проверка добавл. в бд

            store.delete_from_db()  # удаляем из бд

            self.assertIsNone(StoreModel.find_by_name('test'),
                              f"Found a store with name {store.name}, but expected not to")  # проверка удаления из бд

    def test_store_relationship(self):  # test the relationship with items
        with self.app_context():
            store = StoreModel('test')  # новый объект StoreModel
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)  # проверка, что в сторе 1 item
            self.assertEqual(store.items.first().name, 'test_item')  # проверка, что имя 1-го item  в сторе == test_name

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'name': 'test',
            'items': []
        }
        self.assertDictEqual(store.json(), expected)

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 19.99}]}
            self.assertDictEqual(store.json(), expected)
