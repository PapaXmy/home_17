from utils import load_movies, load_genres, load_directors
from app import db



class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


db.drop_all()
db.create_all()

for movie in load_movies():
    m = Movie(
        id=movie["pk"],
        title=movie["title"],
        description=movie["description"],
        trailer=movie["trailer"],
        year=movie["year"],
        rating=movie["rating"],
        genre_id=movie["genre_id"],
        director_id=movie["director_id"],
    )
    with db.session.begin():
        db.session.add(m)

for director in load_directors():
    d = Director(
        id=director["pk"],
        name=director["name"],
    )
    with db.session.begin():
        db.session.add(d)

for genre in load_genres():
    d = Genre(
        id=genre["pk"],
        name=genre["name"],
    )
    with db.session.begin():
        db.session.add(d)
