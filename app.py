import os
from flask import Flask, request, abort, jsonify, render_template
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies, Casting, db
from auth import AuthError, requires_auth, get_token_auth_header
import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    # Access_Control_Allow
    # -----------------------------------
    @app.after_request
    def after_request(response):
        response.headers.add('Access_Control_Allow_Headers', 'Content_Type, Authorization')
        response.headers.add('Access_Control_Allow_Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    @app.route('/')
    def index():
        return render_template('index.html')

    # ---------------------------------------------------
    # ACTORS
    # ---------------------------------------------------

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.all()
            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            })
        except:
            abort(404)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()

            return jsonify({
                'success': True,
                'message': str(actor_id) + ' deleted...'
            })
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        # get the infor from user
        info = request.get_json()

        name = info.get('name', None)
        age = info.get('age', None)
        gender = info.get('gender', None)

        try:
            actor = Actors(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True,
                'message': 'New record has been added !'
            })
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        info = request.get_json()

        new_name = info.get('name', None)
        new_age = info.get('age', None)
        new_gender = info.get('gender', None)

        actor.name = new_name
        actor.age = new_age
        actor.gender = new_gender

        actor.update()

        return jsonify({
            'success': True,
            'actor': 'actor #: ' + str(actor_id) + ' has been edited !'
        })

    # ---------------------------------------------------
    # MOVIES
    # ---------------------------------------------------

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            return jsonify({
                'success': True,
                'actors': [movie.format() for movie in movies]
            })
        except:
            abort(404)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if not movie:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True,
                'message': str(movie_id) + ' deleted...'
            })
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:actors')
    def post_movie(payload):
        # get the infor from user
        info = request.get_json()

        title = info.get('title', None)
        release = info.get('release', None)

        try:
            movie = Movies(title=title, release=release)
            movie.insert()

            return jsonify({
                'success': True,
                'message': 'New record has been added !'
            })
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        info = request.get_json()

        new_title = info.get('title', None)
        new_release = info.get('release', None)

        movie.title = new_title
        movie.release = new_release

        movie.update()

        return jsonify({
            'success': True,
            'movie': 'movie #: ' + str(movie_id) + ' has been edited !'
        })

    # ----------------------------------------------
    # Error Handling
    # ----------------------------------------------

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method is not allowed'
        }), 405


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    #  error handler for AuthError

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
