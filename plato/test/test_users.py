import json

from plato.test.base import BaseTestCase
from plato.api.models import User
from plato import db


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    def test_users(self):
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        '''Ensure a new user can be added to database'''
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='michael',
                    email='michael@realpython.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('michael@realpython.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_invalide_json(self):
        '''Ensure error is thrown if the JSON object is empty'''
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='appilcation/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_invalid_json_key(self):
        '''Ensure error is thrown if the JSON object username key is empty'''
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    email='michael@realpython.com'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_duplicate_user(self):
        '''Ensure error is thrown if user's email already exists'''
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='michael',
                    email='michael@realpython.com'
                )),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='michael',
                    email='michael@realpython.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry, that email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        '''Ensure get single user behaves correctly'''
        user = add_user(username='michael', email='michael@realpython.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@realpython.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        '''Ensure error is thrown if an id is not provided'''
        with self.client:
            response = self.client.get('users/test_id')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        '''Ensure error is thrown if the id is not correct'''
        with self.client:
            response = self.client.get('users/666')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        add_user('michael', 'michael@realpython.com')
        add_user('fletcher', 'fletcher@realpython.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at', data['data']['users'][0])
            self.assertTrue('created_at', data['data']['users'][1])
            self.assertIn('michael', data['data']['users'][0]['username'])
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn('michael@realpython.com', data['data']['users'][0]['email'])
            self.assertIn('fletcher@realpython.com', data['data']['users'][1]['email'])

    def test_main_no_users(self):
        '''Ensure the main route behaves correctly when no users added to database'''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_have_users(self):
        '''Ensure the main route behaves correctly when users have added to database'''
        add_user('michael', 'michael@realpython.com')
        add_user('fletcher', 'fletcher@realpython.com')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertNotIn(b'<p>no users</p>', response.data)
        self.assertIn(b'<strong>michael</strong>', response.data)
        self.assertIn(b'<strong>fletcher</strong>', response.data)

    def test_main_add_user(self):
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='michael', email='michael@realpython.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>no users</p>', response.data)
            self.assertIn(b'<strong>michael</strong>', response.data)
