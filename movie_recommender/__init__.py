from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_recommender.db'
# app.config['UPLOAD_FOLDER'] = '/home/panharith/Documents/Flask/movie_recommender/movie_recommender/static/photos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True     # disable warning
app.config['MAIL_DEFAULT_SENDER'] = "your gmail account"
app.config['MAIL_USERNAME'] = "your gmail account"
app.config['MAIL_PASSWORD'] = "your gmail password"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['SECURITY_PASSWORD_SALT'] = "abcxxx123"

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    from movie_recommender.models import User
    return User.query.filter(User.id == int(user_id)).first()


from movie_recommender import routes, admin_routes
