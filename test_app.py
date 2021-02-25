import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies, Casting, db


test_token = os.environ['producer_token']
low_token = os.environ['assistant_token']

unauthorized = {'code': 'unauthorized', 'description': 'Permission not authorized.'}

class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agencydb"
        db_path = os.environ['DATABASE_URL']
        self.database_path = db_path
        setup_db(self.app, self.database_path)
#        db.create_all()

    def tearDown(self):
        pass

# (1) testing getting actors & movies
    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_in_actors_byID(self):
        res = self.client().get(
            '/actors/1000',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

    def test_not_in_movies_byID(self):
        res = self.client().get(
            '/movies/1000',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

# (2) testing deleting movies & actors :
    def test_delete_actors(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().delete(
            '/actors/{}'.format(actor_id),
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies(self):
        new_movie = Movies(title='the girl', release='1988')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().delete(
            '/movies/{}'.format(movie_id),
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_not_exist(self):
        res = self.client().delete(
            '/actors/1000',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_movies_not_exist(self):
        res = self.client().delete(
            '/movies/1000',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_actors_unauthorized(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().delete(
            '/actors/{}'.format(actor_id),
            headers={'Authorization': 'Bearer ' + low_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

    def test_delete_movies_unauthorized(self):
        new_movie = Movies(title='the girl', release='1988')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().delete(
            '/movies/{}'.format(movie_id),
            headers={'Authorization': 'Bearer ' + low_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

# (3) testing posting new actors & movies
    def test_new_actor(self):
        res = self.client().post(
            '/actors', json={'name': 'Ali', 'age': '25', 'gender': 'male'},
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_new_movie(self):
        res = self.client().post(
            '/movies', json={'title': 'how to do?', 'release': '2003'},
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_actor_adding_notallowed(self):
        res = self.client().post(
            '/actors/45',
            json={'id': '45', 'name': 'memo', 'age': '20', 'gender': 'female'},
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

    def test_405_movie_adding_notallowed(self):
        res = self.client().post(
            '/movies/45',
            json={'id': '45', 'title': 'new release !', 'release': '2005'},
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

    def test_new_actor_unauthorized(self):
        res = self.client().post(
            '/actors',
            json={'name': 'Ali', 'age': '25', 'gender': 'male'},
            headers={'Authorization': 'Bearer ' + low_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

    def test_new_movie_unauthorized(self):
        res = self.client().post(
            '/movies',
            json={'title': 'how to do?', 'release': '2003'},
            headers={'Authorization': 'Bearer ' + low_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

# (4) testing editing actors & movies info
    def test_edit_actor(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().patch(
            '/actors/{}'.format(actor_id),
            json={'name': 'Sara', 'age': '32', 'gender': 'female'},
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_movie(self):
        new_movie = Movies(title='getting in the world!', release='2005')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().patch(
            '/movies/{}'.format(movie_id),
            json={'title': 'getting in the world!', 'release': '1999'},
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_actor_editing_notexist(self):
        res = self.client().patch(
            '/actors/1000',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_movie_editing_notexist(self):
        res = self.client().patch(
            '/movies/1000',
            headers={'Authorization': 'Bearer ' + test_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_edit_actor_unauthorized(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().patch(
            '/actors/{}'.format(actor_id),
            json={'name': 'Sara', 'age': '32', 'gender': 'female'},
            headers={'Authorization': 'Bearer ' + low_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

    def test_edit_movie_unauthorized(self):
        new_movie = Movies(title='getting in the world!', release='2005')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().patch(
            '/movies/{}'.format(movie_id),
            json={'title': 'getting in the world!', 'release': '1999'},
            headers={'Authorization': 'Bearer ' + low_token}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
