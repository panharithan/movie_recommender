from movie_recommender import app, db, migrate
from movie_recommender.models import Movie, User

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Movie=Movie, User=User, migraFte=migrate)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
