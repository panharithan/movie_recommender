from datetime import datetime
from passlib.hash import sha256_crypt
from sqlalchemy import or_
from flask import render_template, url_for, flash, redirect, request, session, flash
from movie_recommender import app
from movie_recommender.forms import LoginForm
from movie_recommender.models import User
from movie_recommender.models import Movie
from movie_recommender import db
from movie_recommender.models import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from tools.token import confirm_token, generate_confirmation_token
from tools.email import send_email


@app.route("/")
@app.route("/home")
def home():

    print(current_user)
    new_movies = []
    for movie in Movie.query.all():
        new_movies.append({
            'title': movie.title,
            'year': movie.year,
            'total_view': movie.total_view,
            'icon': movie.icon,
            'link': movie.link,
            'view_key': movie.view_key,
            'page_link': request.base_url + 'watch?view_key=' + movie.view_key,
            # 'is_active': movie.is_active,

        })
    return render_template('index.html',
                           menus=['Home', 'Contact', 'About', 'Login'],
                           new_movies=new_movies, username=session.get('username'),
                           is_authenticated=current_user.is_authenticated)


@app.route("/watch")
def watch():
    if not session.get('username'):
        return redirect(url_for('login'))
    view_key = request.args.get('view_key', 0)
    if view_key:
        movie = Movie.query.filter_by(view_key=view_key).first()
        if movie:
            link = 'https://drive.google.com/file/d/' + view_key + '/preview'
            return render_template('watch.html', link=link)

    return render_template('watch.html', link=False)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        conds = [User.username == form.username.data, User.email == form.username.data]
        user = User.query.filter(or_(*conds)).first()
        if not user.confirmed:
            error = 'Please confirm your account first.'
            flash(error)
            return render_template('login.html', form=form, error=error)

        if user and sha256_crypt.verify(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            if current_user.is_admin:
                return redirect(url_for('dashboard'))
            return redirect(url_for('home'))

        error = 'Invalid User'
        flash(error)
    return render_template('login.html', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        conds = [User.username == form.username.data, User.email == form.username.data]
        user = User.query.filter(or_(*conds)).first()
        if user:
            return render_template('register.html', form=form,
                                   error="you are already registered")

        new_user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data, is_admin=False)

        db.session.add(new_user)
        db.session.commit()

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)

        return render_template('register.html', form=form, success="Successfully registered. Please confirm your account in Email.")
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return redirect(url_for('login'))
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return render_template('confirm_email.html', error=None, messages={
        'client': user.username if user else 'Client'
    })
