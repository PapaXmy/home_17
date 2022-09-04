import json


def load_movies():

    with open("./data/movies.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


def load_directors():

    with open("./data/directors.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

def load_genres():

    with open("./data/genres.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data



