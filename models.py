from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(
        db.String, nullable=False, default='https://i.stack.imgur.com/l60Hf.png')

    posts = db.relationship('Post', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False,
                        default='This is a post with no content.')
    created_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    tags = db.relationship('Tag', secondary='posts_tags',
                           back_populates='posts')
    post_tags = db.relationship(
        'PostTag', back_populates='post', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post id={self.id} title={self.title} content={self.content} created_at={self.created_at}>'


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post', secondary='posts_tags', back_populates='tags')
    post_tags = db.relationship(
        'PostTag', back_populates='tag', cascade='all, delete-orphan')


class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    post = db.relationship('Post', back_populates='post_tags')
    tag = db.relationship('Tag', back_populates='post_tags')
