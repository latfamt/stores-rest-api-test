from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('test').save_to_db()  # если НЕ sqlite, надо создавать стор, иначе будет ошибка с foreign key
            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')  # create a store
            item = ItemModel('test', 19.99, 1)  # create an item that uses that store
            store.save_to_db()  # save both things to database
            item.save_to_db()

            # then we're going to check that the store name for this item is equal to test_store
            self.assertEqual(item.store.name, 'test_store')
