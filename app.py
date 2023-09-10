from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Post, Tag
from utilities import get_current_date_time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'nfufbo2fif42'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# Initialize flask app to use the database
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    '''Show the home page.'''
    posts = Post.query.order_by(Post.created_at.desc()).all()
    for post in posts:
        post.created_at = post.created_at.strftime('%B %d, %Y, %I:%M %p')
    return render_template('index.html', posts=posts)


@app.route('/users')
def get_all_users():
    '''Show all the users.'''
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def show_add_user_form():
    '''Render a template containing a form for adding a user.'''
    return render_template('add-user.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    '''Process form data to insert user into database.'''
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    image_url = image_url if image_url else None
    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    '''Show details of a particular user.'''
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('user-details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    '''Render template containing a form to edit user.'''
    user = User.query.get(user_id)
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    '''Process form data to edit a particular user in the database.'''
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Delete a particular user from the database.'''
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    '''Render template that allows user to create new post.'''
    user = User.query.get(user_id)
    return render_template('add-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    '''Add a new post for a particular user.'''
    title = request.form['title']
    content = request.form['content']
    content = content if content else None
    created_at = get_current_date_time()
    user_id = user_id
    new_post = Post(title=title, content=content,
                    created_at=created_at, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/users')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    '''Show details of a particular post.'''
    post = Post.query.get(post_id)
    return render_template('post-details.html', post=post, user=post.user)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    '''Render template containing a form to edit a post.'''
    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_form(post_id):
    '''Process form data to edit a post.'''
    title = request.form['title']
    content = request.form['content']
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect('/users')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete a particular post from the database.'''
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')


@app.route('/tags')
def show_tags():
    '''Show all tags.'''
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/new')
def add_tag_form():
    '''Render template to add new tag.'''
    return render_template('add-tag.html')


@app.route('/tags/new', methods=['POST'])
def add_tag():
    '''Process form data to add a new tag.'''
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')
