from movie_recommender.models import Movie
from movie_recommender.models import User
from movie_recommender import db

# pip3 uninstall flask-sqlalchemy
# pip3 install flask-sqlalchemy==2.1.0
#sqlite> ALTER TABLE Movie ADD COLUMN is_trending boolean;

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    movie1 = Movie()
    movie1.title = "John Wick"
    movie1.year = 2014
    movie1.total_view = 0
    movie1.icon = 'static/photos/john_wick1.jpg'
    movie1.link = 'https://drive.google.com/file/d/1yQKxEuqImlgeCobYZNoPl0tlil40WgjZ/preview'
    movie1.view_key = '1yQKxEuqImlgeCobYZNoPl0tlil40WgjZ'


    movie2 = Movie()
    movie2.title = "John Wick: Chapter 2"
    movie2.year = 2017
    movie2.total_view = 0
    movie2.icon = 'static/photos/john_wick2.jpg'
    movie2.link = 'https://drive.google.com/file/d/1B8yB_ycfLM2mjNImA-TljIZg1CL_3PUE/preview'
    movie2.view_key = '1B8yB_ycfLM2mjNImA-TljIZg1CL_3PUE'

    movie3 = Movie()
    movie3.title = "John Wick: Chapter 3 – Parabellum"
    movie3.year = 2019
    movie3.total_view = 0
    movie3.icon = 'static/photos/john_wick3.jpg'
    movie3.link = 'https://drive.google.com/file/d/1psJNIRL-u28WUZTcERDGH07tzt4nuj5R/preview'
    movie3.view_key = '1psJNIRL-u28WUZTcERDGH07tzt4nuj5R'

    movie4 = Movie()
    movie4.title = "Batman Begins"
    movie4.year = 2005
    movie4.total_view = 0
    movie4.icon = 'static/photos/batman1.jpg'
    movie4.link = 'https://drive.google.com/file/d/1jThyoa3lApPFyGnKn04WHSaIyKYP5gRD/preview'
    movie4.view_key = '1jThyoa3lApPFyGnKn04WHSaIyKYP5gRD'

    # movie5 = Movie()
    # movie5.title = "The Dark Knight"
    # movie5.year = 2008
    # movie5.total_view = 0
    # movie5.icon = 'static/photos/batman2.jpg'
    # movie5.link = 'https://www.youtube.com/watch?v=EXeTwQWrcwY'
    # movie5.view_key = 'EXeTwQWrcwY'
    #
    # movie6 = Movie()
    # movie6.title = "The Dark Knight Rises"
    # movie6.year = 2012
    # movie6.total_view = 0
    # movie6.icon = 'static/photos/batman3.jpg'
    # movie6.link = 'https://www.youtube.com/watch?v=GokKUqLcvD8'
    # movie6.view_key = 'GokKUqLcvD8'

    db.session.add(movie1)
    db.session.add(movie2)
    db.session.add(movie3)
    db.session.add(movie4)
    # db.session.add(movie5)
    # db.session.add(movie6)
    db.session.commit()
    for movie in Movie.query.all():
        print(movie)
    for user in User.query.all():
        print(user)
