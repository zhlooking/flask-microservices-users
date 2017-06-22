from sqlalchemy.exc import IntegrityError

from plato import db
from plato.api.models import User
from plato.test.base import BaseTestCase
from plato.test.utils import add_user


class TestUserModel(BaseTestCase):
    def test_user_model(self):
        user = add_user('foo', 'foo@bar.com', 'test_pwd')
        self.assertTrue(user.id)
        self.assertEqual('foo', user.username)
        self.assertEqual('foo@bar.com', user.email)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        duplicate_user = User('foo', 'foo_1@bar.com', 'test_pwd')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        duplicate_user = User('foo_1', 'foo@bar.com', 'test_pwd')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_foo = add_user('foo', 'foo@bar.com', 'test_pwd')
        user_bar = add_user('bar', 'bar@bar.com', 'test_pwd')
        self.assertNotEqual(user_foo.password, user_bar.password)
