from models import db, User, Post, Tag, PostTag
from app import app
from utilities import get_current_date_time

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

with app.app_context():
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()
    PostTag.query.delete()

# Add users
john = User(first_name='John', last_name='Doe', image_url=None)
jane = User(first_name='Jane', last_name='Doe', image_url=None)
jill = User(first_name='Jill', last_name='Doe', image_url=None)

post1 = Post(title='First Post', user_id=1, created_at=get_current_date_time())
post2 = Post(title='Second Post', user_id=1,
             created_at=get_current_date_time())
post3 = Post(title='Third Post', user_id=1, created_at=get_current_date_time())

fun = Tag(name='Fun')
even_more = Tag(name='Even More')
bloop = Tag(name='Bloop')
zope = Tag(name='Zope')

data_initial = [john, jane, jill, post1,
                post2, post3, fun, even_more, bloop, zope]
with app.app_context():
    db.session.add_all(data_initial)
    db.session.commit()
    post1_fun = PostTag(post_id=post1.id, tag_id=fun.id)
    post1_bloop = PostTag(post_id=post1.id, tag_id=bloop.id)

# Add and commit PostTag associations
with app.app_context():
    # Now, create PostTag associations
    db.session.add(post1_fun)
    db.session.add(post1_bloop)
    db.session.commit()
