from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///blogly_test'

with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTestCase(TestCase):
    '''Tests for models for users.'''

    def setUp(self):
        '''Clean up any existing users.'''
        with app.app_context():
            User.query.delete()

    def test_get_full_name(self):
        user = User(first_name='John', last_name='Doe', image_url='')
        self.assertEqual(user.get_full_name(), 'John Doe')
