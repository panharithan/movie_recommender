from passlib.hash import sha256_crypt
from movie_recommender import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField, IntegerField

from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from movie_recommender import login_manager
from wtforms.widgets import html5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_user.png')
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def __init__(self, username, email, password, confirmed=False, is_admin=False):
        self.username = username
        self.email = email
        self.password = sha256_crypt.encrypt(password)
        self.is_admin = is_admin
        self.confirmed = confirmed


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    year = db.Column(db.Integer)
    total_view = db.Column(db.Integer)
    icon = db.Column(db.String(64), nullable=True, default='static/default_icon.jpg')
    link = db.Column(db.String(1000), nullable=True)
    view_key = db.Column(db.String(1000), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_trending = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Movie('{self.id}', " \
            f"'{self.title}'," \
            f"'{self.year}'," \
            f"'{self.total_view}'," \
            f"'{self.link}'," \
            f"'{self.view_key}'," \
            f" '{self.date_posted}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class MovieForm(FlaskForm):

    title = StringField('Title', validators=[InputRequired(), Length(min=1, max=50)])
    year = IntegerField('Year', widget=html5.NumberInput(), default=datetime.now().year)
    link = StringField('Link', validators=[InputRequired(), Length(min=1, max=1000)])
    view_key = StringField('View Key', validators=[Length(min=1, max=1000)])
    is_trending = BooleanField('Is Trending')
