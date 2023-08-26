from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()


class UserViewsTestCase(TestCase):
    '''Tests for views for users.'''

    def setUp(self):
        '''Add a sample user.'''
        with app.app_context():
            User.query.delete()
            user = User(first_name='John', last_name='Doe')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id
            self.user = user

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
