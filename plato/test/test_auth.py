import json
import datetime

from plato.test.utils import add_user
from plato.test.base import BaseTestCase


class TestAuthService(BaseTestCase):
    def test_user_registeration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps(dict(
                    username='foo',
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data=json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
