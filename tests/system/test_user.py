from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    # we want to test that we can register a user
    def test_register_user(self):
        with self.app() as client:  # чтоб делать запросы
            with self.app_context():  # чтоб обращаться к БД
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))  # убедиться, что json-ответ переконв. в python-dict

    # we also want to test that we can log in
    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                # /auth requires that we're sending the data in json format, it doesn't accept FORM format

                self.assertIn('access_token', json.loads(auth_response.data).keys())  # ['access_token'] in response

    # error when user is already exists
    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))

