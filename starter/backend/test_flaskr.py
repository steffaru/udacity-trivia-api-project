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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '123456', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_quetions = {
            'question' : 'Which team won the NBA Championship in 2004?',
            'answer' : 'Detroit Pistons',
            'category' : 6,
            'difficulty' : 3
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # def test_get_paginated_questions(self):
    #     res = self.client().get('http://localhost:5000/api/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['questions']))

    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get('http://localhost:5000/api/questions?page=1000', json={'difficulty': 5})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_delete_question(self):
    #     res = self.client().delete('http://localhost:5000/api/questions/1')
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 1).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(question, None)

    # def test_404_if_question_doesnt_exist(self):
    #     res = self.client().delete('http://localhost:5000/api/questions/1000')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_post_created_questions(self):
    #     res = self.client().post('http://localhost:5000/api/questions/create', json={'question' : 'Which team won the NBA Championship in 2002?','answer' : 'The Lakers','category' : 6,'difficulty' : 3}, headers={'Content-Type': 'application/json'})
    #     questions = Question.query.all()
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(questions))

    #FALTA TEST 422 O 405 0 404

    # def test_post_searched_words(self):
    #     search = 'Which'
    #     res = self.client().post('http://localhost:5000/api/questions/search', json={'searchTerm' : search}, headers={'Content-Type': 'application/json'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['search'], search)

        #FALTA TEST 404


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()