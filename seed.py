from models import db, User, Post
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()


# Add users
john = User(first_name='John', last_name='Doe', image_url=None)
jane = User(first_name='Jane', last_name='Doe', image_url=None)
jill = User(first_name='Jill', last_name='Doe', image_url=None)

post1 = Post(title='First Post', user_id=1)
post2 = Post(title='Second Post', user_id=1)
post3 = Post(title='Third Post', user_id=1)

data = [john, jane, jill, post1, post2, post3]

with app.app_context():
    # Add all objects to the session
    db.session.add_all(data)
    db.session.commit()
