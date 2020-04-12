import os
from flask import render_template, url_for, flash, redirect, request, session, flash
from movie_recommender import app
from movie_recommender.forms import LoginForm
from movie_recommender.models import User
from movie_recommender.models import Movie, MovieForm
from movie_recommender import db
from movie_recommender.models import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_file(files):
    for file in files:
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('login'))
    flash("welcome back sir")
    movies = []
    for movie in Movie.query.all():
        movies.append({
            'id': movie.id,
            'title': movie.title,
            'year': movie.year,
            'total_view': movie.total_view,
            'icon': movie.icon,
            'link': movie.link,
            'view_key': movie.view_key,
            'date_posted': movie.date_posted,
            'is_trending': movie.is_trending or False,
        })

    return render_template('dashboard.html', movies=movies)


@app.route('/new_movie', methods=['GET', 'POST'])
@login_required
def new_movie():
    if not current_user.is_admin:
        return redirect(url_for('login'))
    form = MovieForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # if user does not select file, browser also
            # submit a empty part without filename
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            path, icon = '', ''
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print("######## path: ", path)
                icon = 'static/photos/' + filename
                file.save(path)

            movie1 = Movie()
            movie1.title = request.form['title']
            movie1.year = request.form['year']
            movie1.total_view = 0
            movie1.icon = icon
            movie1.link = request.form['link']
            movie1.view_key = ''
            db.session.add(movie1)
            db.session.commit()
            for movie in Movie.query.all():
                print(movie)

    return render_template('new_movie.html', form=form, error=False)
