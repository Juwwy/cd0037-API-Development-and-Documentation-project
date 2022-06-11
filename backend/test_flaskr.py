import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.db_username = 'student'
        self.db_password = 'student'
        self.db_url = 'localhost:5432'
        self.database_path = 'postgres://{}:{}@{}/{}'.format(self.db_username, self.db_password, self.db_url, self.database_name)
        # 'postgres://{}:{}@{}/{}'.format(self.db_username, self.db_password, db_url, database_name)
        setup_db(self.app, self.database_path)

        # self.new_question = {
        #     "question" : "The tall mountain on earth is?",
        #     "answer": "Kilimanjaro",
        #     "category": "1",
        #     "difficulty" : 3
        # }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # def test_given_behavior(self):
    #     """hjfj"""
    #     res = self.client().get('/questions')

    #     self.assertEqual(res.status_code, 200)

    def test_get_paginated_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_404_sent_not_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'difficulty' : 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()