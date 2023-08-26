from models import db, User
from app import app

with app.app_context():
    # Create tables
    db.drop_all()
    db.create_all()

    # Empty table if it isn't already empty.
    User.query.delete()


# Add users
john = User(first_name='John', last_name='Doe', image_url=None)
jane = User(first_name='Jane', last_name='Doe', image_url=None)
jill = User(first_name='Jill', last_name='Doe', image_url=None)

users = [john, jane, jill]

with app.app_context():
    # Add all objects to the session
    db.session.add_all(users)
    db.session.commit()
