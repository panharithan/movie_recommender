from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_recommender.db'
app.config['UPLOAD_FOLDER'] = '/home/panharith/Documents/Flask/movie_recommender/movie_recommender/static/photos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True     # disable warning


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)

from movie_recommender import routes, admin_routes
