import unittest

from flask_script import Manager
from plato import create_app, db
from plato.api.models import User


app = create_app()
manager = Manager(app)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def test():
    ''' Run tests without code coverage '''
    tests = unittest.TestLoader().discover('plato/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def seed_db():
    '''Seeds the database'''
    db.session.add(User('michael', 'michael@realpython.com'))
    db.session.add(User('michaelherman', 'michaelherman@realpython.com'))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
