from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from models import *
from schems import *



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

@movies_ns.route('/')
class MovieViews(Resource):
    def get(self):
        query = db.session.query(Movie)

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id is not None:
           query = query.filter(Movie.director_id == director_id)
        if genre_id is not None:
           query = query.filter(Movie.genre_id == genre_id)
        all_movies = query.all()
        return movies_schema.dump(all_movies), 200



@movies_ns.route('/<int:mov_id>')
class MovieViews(Resource):
    def get(self, mov_id):
        movie = db.session.query(Movie).filter(Movie.id == mov_id).one()
        if movie is None:
            return "Фильм не найден", 404

        return movie_schema.dump(movie)

@directors_ns.route('/')
class DirectorsViews(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        if directors is None:
            return "Режиссер не найден", 404

        return directors_schema.dump(directors)

    def post(self):
        dir_json = request.json
        new_director = Director(**dir_json)
        with db.session.begin():
            db.session.add(new_director)

        return "Режисер добавлен", 201


@directors_ns.route('/<int:dir_id>')
class DirectorView(Resource):
    def get(self, dir_id):
        director = db.session.query(Director).get(dir_id)
        if director is None:
            return "Режиссер не найден", 404

        return director_schema.dump(director)


    def put(self, dir_id):
        director = db.session.query(Director).get(dir_id)
        dir_json = request.json

        director.name = dir_json.get("name")

        db.session.add(director)
        db.session.commit()

        return "Данные о режиссере обновлены", 200

    def delete(self, dir_id):
        director = db.session.query(Director).get(dir_id)

        db.session.delete(director)
        db.session.commit()

        return "Данные о режиссере обновлены", 204


@genres_ns.route('/')
class GenresViews(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        if genres is None:
            return "Жанр не найден", 404

        return genres_schema.dump(genres)

    def post(self):
        gen_json = request.json
        new_genre = Genre(**gen_json)
        with db.session.begin():
            db.session.add(new_genre)

        return "Добавлен новый жанр", 201


@genres_ns.route('/<int:gen_id>')
class GenreViews(Resource):
    def get(self, gen_id):
        genre = db.session.query(Genre).get(gen_id)
        if genre is None:
            return "Жанр не найден", 404

        return genre_schema.dump(genre)


    def put(self, gen_id):
        genre = db.session.query(Genre).get(gen_id)
        gen_json = request.json

        genre.name = gen_json.get("name")

        db.session.add(genre)
        db.session.commit()

        return "Данные о жанре обновленны", 200

    def delete(self, gen_id):
        genre = db.session.query(Genre).get(gen_id)

        db.session.delete(genre)
        db.session.commit()

        return "Данные о жанре удалены"

if __name__ == "__main__":
    app.run()



