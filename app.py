from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
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
    return render_template('index.html')


@app.route('/users')
def get_all_users():
    '''Show all the users.'''
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def add_new_user():
    '''Render a template containing a form for adding a user.'''
    return render_template('add-user.html')
