import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies, Casting, create_db

unauthorized = {'code': 'unauthorized', 'description': 'Permission not authorized.'}

test_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InkzeG45Tks0WVFRY1BoX1JnUEg2XyJ9.eyJpc3MiOiJodHRwczovL2Rldi1raGFkaWphLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDMyOGEzYzkwZTQ0MjAwNzAzOTIxM2MiLCJhdWQiOiJjcHN0biIsImlhdCI6MTYxNDA5OTk2NiwiZXhwIjoxNjE0MTg2MzY2LCJhenAiOiJuVjBNMFZFUmFnN3BrcDByemY0eGowR3gxRmQ4OUhpbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.AMPxDlkiLS2RBFvH0Mw-yGo_PW4R74WIZUQsy4XagvFUvW8-VPdR47KfWPLE5OMFrcfoRzCm9Z-7kvJk6mUI3FI9DDO5pustsjdFpElGXu3crOqseS7dD7Ih68no2E1Vzg5M1diZxaPLEg8_GKmWl_NzAbgsBMCC6DBog4QtCiJvOpq59JtnD-xrzqTjPkU0qJAALOiI4k_PoPe8GF8KlxnV6n-rEmFkC9srXbVvCAymjM9vCBhFHeepk7OGlmIftKOWDe5W_wczTkV382SdryzfuZnlkU4J0T_QVFAVl1Yf2WDbQ8fx_mBf94eLZ90YpiIEDXSPjdK2FF2nONFMDw'

low_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InkzeG45Tks0WVFRY1BoX1JnUEg2XyJ9.eyJpc3MiOiJodHRwczovL2Rldi1raGFkaWphLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDMyODk5YThmZWEzZTAwNjg2Y2NjMWYiLCJhdWQiOiJjcHN0biIsImlhdCI6MTYxNDEwMDEzNCwiZXhwIjoxNjE0MTg2NTM0LCJhenAiOiJuVjBNMFZFUmFnN3BrcDByemY0eGowR3gxRmQ4OUhpbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.neuw_F-MjuALiJQNjyXzP4ypkJmzmzWwS_V6bGjsI7aBnFsy-KSljEbwZ_AAscXY0Sh8fv27GMZAEJxQ_iYxj72QwNAc6idqFK4MfTItPmN-rj_JM1-TuViMudGoHHq-rNR6ljvQntwrbmDX1VLzxxp3w_WhjY4qxmqTcXAOoQ4rBl0xveeo9DC8XxAOE5p198KcvtDWOozo2MqTf9_Y_knibL7eR8hqpjhxlWl88jcq1h2ys9gPtnJsCY_GczN8X4KjitZCrYuqpWeYqY56xYoqjYu61WcxBYhm6JXi7iI7EPMuRDXhLNyN-xO6p9LIGEuGmQvxO2-AHzJhmL8q3w'

class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agencytest"
        self.database_path = "postgres://qrilylmeeszxvk:bf709eb5cdd58b8f6ad8d1ee4a7f5ae2c2b9287450b6a160ca0679598804677f@ec2-54-211-77-238.compute-1.amazonaws.com:5432/dfquadfsgqpndg"
        setup_db(self.app, self.database_path)


    def tearDown(self):
        pass

# (1) testing getting actors & movies
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_in_actors_byID(self):
        res = self.client().get('/actors/1000', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

    def test_not_in_movies_byID(self):
        res = self.client().get('/movies/1000', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

# (2) testing deleting movies & actors :
    def test_delete_actors(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().delete('/actors/{}'.format(actor_id), headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies(self):
        new_movie = Movies(title='the girl', release='1988')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().delete('/movies/{}'.format(movie_id), headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_not_exist(self):
        res = self.client().delete('/actors/1000', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_movies_not_exist(self):
        res = self.client().delete('/movies/1000', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_actors_unauthorized(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().delete('/actors/{}'.format(actor_id), headers={'Authorization': 'Bearer ' + low_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

    def test_delete_movies_unauthorized(self):
        new_movie = Movies(title='the girl', release='1988')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().delete('/movies/{}'.format(movie_id), headers={'Authorization': 'Bearer ' + low_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

# (3) testing posting new actors & movies
    def test_new_actor(self):
        res = self.client().post('/actors', json={'name': 'Ali', 'age': '25', 'gender': 'male'}, headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_new_movie(self):
        res = self.client().post('/movies', json={'title': 'how to do?', 'release': '2003'}, headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_actor_adding_notallowed(self):
        res = self.client().post('/actors/45', json={'id': '45', 'name': 'memo', 'age': '20', 'gender': 'female'}, headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

    def test_405_movie_adding_notallowed(self):
        res = self.client().post('/movies/45', json={'id': '45', 'title': 'new release !', 'release': '2005'}, headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

    def test_new_actor_unauthorized(self):
        res = self.client().post('/actors', json={'name': 'Ali', 'age': '25', 'gender': 'male'}, headers={'Authorization': 'Bearer ' + low_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

    def test_new_movie_unauthorized(self):
        res = self.client().post('/movies', json={'title': 'how to do?', 'release': '2003'}, headers={'Authorization': 'Bearer ' + low_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

# (4) testing editing actors & movies info
    def test_edit_actor(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().patch('/actors/{}'.format(actor_id), json={'name': 'Sara', 'age': '32', 'gender': 'female'}, headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_movie(self):
        new_movie = Movies(title='getting in the world!', release='2005')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().patch('/movies/{}'.format(movie_id), json={'title': 'getting in the world!', 'release': '1999'}, headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_actor_editing_notexist(self):
        res = self.client().patch('/actors/1000', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_movie_editing_notexist(self):
        res = self.client().patch('/movies/1000', headers={'Authorization': 'Bearer ' + test_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_edit_actor_unauthorized(self):
        new_actor = Actors(name='Sara', age='35', gender='female')
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().patch('/actors/{}'.format(actor_id), json={'name': 'Sara', 'age': '32', 'gender': 'female'}, headers={'Authorization': 'Bearer ' + low_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)

    def test_edit_movie_unauthorized(self):
        new_movie = Movies(title='getting in the world!', release='2005')
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().patch('/movies/{}'.format(movie_id), json={'title': 'getting in the world!', 'release': '1999'}, headers={'Authorization': 'Bearer ' + low_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], unauthorized)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
