from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/teststore')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('teststore'))
                self.assertDictEqual({'name': 'teststore', 'items': []},
                                     json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore')
                response = client.post('/store/teststore')
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {
                        'message': "A store with name 'teststore' already exists."
                    },
                    json.loads(response.data)
                )

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore') # можно также StoreModel('teststore').save_to_db()
                self.assertIsNotNone(StoreModel.find_by_name('teststore'))
                response = client.delete('/store/teststore')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'},
                                     json.loads(response.data))
                self.assertIsNone(StoreModel.find_by_name('teststore'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore')
                response = client.get('/store/teststore')
                self.assertEqual(response.status_code, 200)
                expected = {
                    'name': 'teststore',
                    'items': []
                }
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/teststore')
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))
                self.assertEqual(response.status_code, 404)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore')
                client.post('/item/testitem', data={'price': 19.99, 'store_id': 1}) # or ItemModel('testitem', 19.99, 1).save_to_db()
                response = client.get('/store/teststore')
                expected = {'name': 'teststore',
                            'items': [{'name': 'testitem', 'price': 19.99}]
                            }
                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 200)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore_one')
                client.post('/store/teststore_two')

                storelist=client.get('/stores')
                expected = {'stores': [
                    {'name': 'teststore_one', 'items': []},
                    {'name': 'teststore_two', 'items': []}
                ]
                }
                self.assertDictEqual(json.loads(storelist.data), expected)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore_one')
                client.post('/store/teststore_two')
                client.post('/item/itemforone', data={'price':19.99, 'store_id': 1})
                client.post('/item/itemfortwo', data={'price': 29.99, 'store_id': 2})

                storelist = client.get('/stores')
                expected = {'stores': [
                    {'name': 'teststore_one', 'items': [{'name': 'itemforone', 'price': 19.99}]},
                    {'name': 'teststore_two', 'items': [{'name': 'itemfortwo', 'price': 29.99}]}
                ]
                }
                self.assertDictEqual(json.loads(storelist.data), expected)

