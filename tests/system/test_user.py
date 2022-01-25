from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                #testuje resources/user.py
                self.assertEqual(response.status_code, 201)  # sprawdza po request kodzie
                self.assertIsNotNone(UserModel.find_by_username('test'))    # sprawdza po nazwie
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(response.data))  # sprawdza po wiadomosci

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())  # ['access_token']

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})              # pierwsze żądanie
                response = client.post('/register', data={'username': 'test', 'password': '1234'})   # drugie żądanie

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'An user with that username already exists'}, json.loads(response.data))