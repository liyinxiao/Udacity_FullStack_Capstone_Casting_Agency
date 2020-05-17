import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

assistant_token = "Bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJOanhwdE5vQUI4V0JrVnRhUGg4bSJ9.eyJpc3MiOiJodHRwczovL2Rldi04M2hyanUtaC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNmRlZDk1NGIxNGMwYzEyODk1YWMxIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE1ODk2NjIxMTgsImV4cCI6MTU4OTc0ODUxOCwiYXpwIjoidnQyVWxiQXdmd29HOWtTME1JS3pTb2dDWTlrNEkzOHIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.FdKFMq3AUKY4dRTQuuTAoFYSJ0aWdRJi_yc8Q_iwDLrcWVNokZoHZ7ONtyKUpOn27CuCswsAKrtQR6I19nzqZ5WMmy28vPjctt7m4m5IQWY3mSBviBnb88SZC7gj9Pu_3ruQ8Fj9yqqMKCUoKksUsLtBxA8AG_7lgdnqFoRiaX0-SIHaWwJoSlFomPLxabELJXnPpypNnXKyUetMnHJEvCaM2pnDyh_ZBGBsUgS2TI3oe60ADc-dwmu7pVYIjfUW-76hW-DcjDav3IT7eLfCk5hGVo5SQ5tl-HW4pMD3ZOholJvqK3IPNAQnZpZwGNOO5KZGurobEhRqfrA5rE5fhQ")
director_token = "Bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJOanhwdE5vQUI4V0JrVnRhUGg4bSJ9.eyJpc3MiOiJodHRwczovL2Rldi04M2hyanUtaC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNmRlOTgxY2MxYWMwYzE0OTgwNWU4IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE1ODk2NjE3NDEsImV4cCI6MTU4OTc0ODE0MSwiYXpwIjoidnQyVWxiQXdmd29HOWtTME1JS3pTb2dDWTlrNEkzOHIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.kqUzQdFON0WBS4RTs5GOLDUlb5mMPGGDAOjI5BP7uEbFOOg2WOgRM_WQr2HfrSoUruojhO7D2NMrZxa3XyZBCp8d0hUrPdQOsbN9sDeJthX008tq5457F91TrAC7XJpkvKh065T2aYXJgsWpOBly9RFI4TuxPiG-vTOzeXPfLp898T4Og25pmBRSOFuV9OivZvGqW2k7085lQ8UMHOlQTazxz1lo9VSKAd3YPnphj6-tEHE5SQ7bIu1AnD85uQQXwu4uuy420Ya0nV2h5gMIvmdij1nW9FtWC43QnAdhwvTzU8A9Ru5VJXwXQIHQ7uXgNuWkZWuEPp1hMXxu0gjrng")
producer_token = "Bearer {}".format("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJOanhwdE5vQUI4V0JrVnRhUGg4bSJ9.eyJpc3MiOiJodHRwczovL2Rldi04M2hyanUtaC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjMDRkNWQ0NTNlMjMwYzcxZDcwY2QwIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE1ODk2NjE1OTMsImV4cCI6MTU4OTc0Nzk5MywiYXpwIjoidnQyVWxiQXdmd29HOWtTME1JS3pTb2dDWTlrNEkzOHIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.bWq99IU2hOTS8uLUUpnBtvEPJw5ziQaRgtJMzXFjQwwsineWBMud86wAUkjTajtvn5KHL4LIwwprGkXXkNgcMp74OkdtQA3eGk2gDA9SuiEM-iZmoP0U4y5KmCoBGMxPqM-VHjxwpG1_mIYtJi56DgoV2UR-m6fWa7TJaFiKg04xwWTMbcbkDGo-tH3CAYKs1mGCs5Eu30DD2fzKStWjT0YaDTm2AzE3SOdtIllycEIGUr1cWmCC_hm_LFBSUmnQYj3QW-tL_vt8ab3AsPniHDOn6XcJ7G7_WhXWAUZ8k6pgVi9Cnb8QrWRxppMeczjqTnqRWQa3lhyMqxvUKNn1qQ")

class CastingAgencyTestCase(unittest.TestCase):
  """This class represents the Casting Agency test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "casting_agency"
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()


    self.new_actor = {
      'name': 'actor1',
      'age': 20,
      'gender': 'Male'
    }

    self.new_actor_2 = {
      'name': 'actor2',
      'age': 20,
      'gender': 'Male'
    }

    self.update_actor = {
      'name': 'updated_actor',
      'age': 20,
      'gender': 'Female'
    }

    self.new_movie = {
      'title': 'movie1',
      'release_date': '2020-01-01'
    }

    self.new_movie_2 = {
      'title': 'movie2',
      'release_date': '2020-01-01'
    }

    self.update_movie = {
      'title': 'updated_movie',
      'release_date': '2020-01-01'
    }

  def tearDown(self):
    """Executed after reach test"""
    pass

  def test_get_actors(self):
    res = self.client().get('/actors', headers={"Authorization": assistant_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) >= 0)

  def test_get_movies(self):
    res = self.client().get('/movies', headers={"Authorization": assistant_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) >= 0)

  def test_create_actors(self):
    res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": director_token})
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) == 1)

  def test_create_movies(self):
    res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) == 1)

  def test_update_actors(self):
    self.client().post('/actors', json=self.new_actor, headers={"Authorization": producer_token})
    res = self.client().patch('/actors/1', json=self.update_actor, headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) == 1)

  def test_update_movies(self):
    self.client().post('/movies', json=self.new_movie, headers={"Authorization": director_token})
    res = self.client().patch('/movies/1', json=self.update_movie, headers={"Authorization": director_token})
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) == 1)

  def test_delete_actors(self):
    self.client().post('/actors', json=self.new_actor, headers={"Authorization": producer_token})
    self.client().post('/actors', json=self.new_actor_2, headers={"Authorization": producer_token})
    res = self.client().delete('/actors/2', headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['delete'], '2')
    self.assertTrue(data['success'])

  def test_delete_movies(self):
    self.client().post('/movies', json=self.new_movie, headers={"Authorization": producer_token})
    self.client().post('/movies', json=self.new_movie_2, headers={"Authorization": producer_token})
    res = self.client().delete('/movies/2', headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['delete'], '2')
    self.assertTrue(data['success'])

  def test_401_get_actors (self):
    res = self.client().get('/actors')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_get_movies (self):
    res = self.client().get('/movies')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_create_actors (self):
    res = self.client().post('/actors', json=self.new_actor)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_create_movies (self):
    res = self.client().post('/movies', json=self.new_movie)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_404_update_actors (self):
    res = self.client().patch('/actors/10000', json=self.update_actor, headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

  def test_404_update_movies (self):
    res = self.client().patch('/movies/10000', json=self.update_movie, headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

  def test_404_delete_actors (self):
    res = self.client().delete('/actors/10000', headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

  def test_404_delete_movies (self):
    res = self.client().delete('/movies/10000', headers={"Authorization": producer_token})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

if __name__ == "__main__":
  unittest.main()
