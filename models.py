import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# database config:
# ---------------------
database_name = "agencydb"
database_path = os.environ['DATABASE_URL']

# config
# ---------------------
db = SQLAlchemy()


# DB SETUP
# -----------------------
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# ----------------------------------------------------------------------------#
# MODELS
# ----------------------------------------------------------------------------#
# Movies
class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release = db.Column(db.String(20), nullable=False)
    cast = db.relationship('Casting', backref='title', lazy=True)

    def __init__(self, title, release):
        self.title = title
        self.release = release

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release
        }


# Actors
class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20))
    cast = db.relationship('Casting', backref='actor_name', lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


# Casting: the relationsip table between the Actors and Movies
class Casting(db.Model):
    __tablename__ = 'Casting'

    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.Integer, db.ForeignKey('Movies.id'), nullable=False)
    actor = db.Column(db.Integer, db.ForeignKey('Actors.id'), nullable=False)

    def __init__(self, movie, actor):
        self.movie = movie
        self.actor = actor

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie': self.movie,
            'actor': self.actor
        }
