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
        setup_db(self.app, self.database_path)

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

    #================= Question Test =========
    def test_get_paginated_question(self):
        res = self.client().get('/api/v1/questions')
        data = json.loads(res.data)
        print(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']), 19)

    def test_404_sent_not_valid_page(self):
        res = self.client().get('/api/v1/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    #======== Question Search =========

    def test_search_question(self):
        res = self.client().post('/api/v1/questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_no_search_question(self):
        res = self.client().post('/api/v1/questions/search', json={"searchTerm": "jug"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    #======== Question Create ===============

    def test_create_question(self):
        res = self.client().post('/api/v1/questions', json={"question" : "fastest animal in jungle?", "answer": "cheetah", "difficulty": 3, "category": "4"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'created successful')
   
    def test_not_created_question(self):
        res = self.client().post('/api/v1/questions', json={"question": 123, "answer": None, "difficulty":3, "category":3})
        data = json.loads(res.data)
        #======= NOTED ============
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], 'created successful')

    #===== Question Delete ==============

    def test_delete_question(self):
        res = self.client().delete(f'/api/v1/questions/{12}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted successfully!')

    def test_delete_question_not_found(self):
        res = self.client().delete(f'/api/v1/questions/{450}' )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    #========== Update Question ===========

    # def test_update_question(self):
    #     res = self.client().put(f'/api/v1/questions/{12}/update',  json={ "question": "1234 is a ___", "answer": "numbers", "category": '3', "difficulty": 2})
    #     data = json.loads(res.data)
    #     #quest = Question.query.filter(Question.id == 27).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['message'], 'Update was successful!')

    # def test_not_updated_question(self):
    #     res = self.client().put(f'/api/v1/questions/{24}/update', json={"q1": "", "q2":"", "q3":0, "q4":""})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Oops! your request can\'t be processed. Internal server error')

    
    #============ Play Quiz =============

    def test_play_quiz(self):
        self.play_quiz_option = {
            "previous_questions": [3],
            "quiz_category": {'id':3, 'type': 'Geography'}
        }
        res = self.client().post('/api/v1/quizzes', json=self.play_quiz_option)
        #data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertIn('question', res.get_json())

    
    def test_not_play_quiz(self):
        self.play_quiz_option = {
            "previous_questions": [3],
            "quiz_category": {'id':89, 'type': 'verbal'}
        }
        res = self.client().post('/api/v1/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        #self.assertFalse(data['question'])

    

    #=============== Categories Test ==================

    def test_get_categories(self):
        response = self.client().get('/api/v1/categories/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))
    
    def test_no_category(self):
        res = self.client().get('/api/v1/categories/page')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()