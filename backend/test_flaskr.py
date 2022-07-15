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
        self.database_path = "postgresql://{}{}/{}".format('postgres:abc','@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question' : 'Which African footballer ever won the world player?',
            'answer': 'Finidi George',
            'category': 6,
            'difficulty' : 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        res=self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        

    def test_404_get_paginated_questions_failed(self):
        res = self.client().get('/questions?page=5')
        data = json.loads(res.data)
        

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

    def test_422_failed_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)


    def test_delete_question(self):
        res = self.client().delete('/questions/25')
        data = json.loads(res.data)

    def test_404_delete_questions_failed(self):
        res = self.client().delete('/questions/25')
        data = json.loads(res.data)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()