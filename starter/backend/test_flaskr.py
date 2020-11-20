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
    def test_get_paginated_questions(self):
        res = self.client().get('http://localhost:5000/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('http://localhost:5000/api/questions?page=1000', json={'difficulty': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_question(self):
        res = self.client().delete('http://localhost:5000/api/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_404_if_question_doesnt_exist(self):
        res = self.client().delete('http://localhost:5000/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_post_created_questions(self):
        res = self.client().post('http://localhost:5000/api/questions/create', json={'question' : 'Which team won the NBA Championship in 2002?','answer' : 'The Lakers','category' : 6,'difficulty' : 3}, headers={'Content-Type': 'application/json'})
        questions = Question.query.all()
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions))

    def test_422_if_create_question_is_unprocessable(self):
        res = self.client().post('http://localhost:5000/api/questions/create', json={'question': '','category' : 'rrr','difficulty' : 3}, headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_post_searched_words(self):
        search = 'Which'
        res = self.client().post('http://localhost:5000/api/questions/search', json={'searchTerm' : search}, headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['search'], search)

    def test_404_if_word_doesnt_exist(self):
        search = 'esternocleidomastoideo'
        res = self.client().post('http://localhost:5000/api/questions/search', json={'searchTerm' : search}, headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_questions_by_categories(self):
        res = self.client().get('http://localhost:5000/api/category/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_categories'])

    def test_404_if_category_doesnt_exist(self):
        question_category = '1'
        res = self.client().get('http://localhost:5000/api/category/question_category/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_post_quiz_questions(self):
        quiz_category = 2
        res = self.client().post('http://localhost:5000/api/quizzes', json={'previous_questions' : [1,2], 'quiz_category': quiz_category}, headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['previous_question'])

    def test_404_if_previous_question_doesnt_exist(self):
        previous_questions = []
        quiz_category = 1000
        res = self.client().post('http://localhost:5000/api/quizzes', json={'previous_questions' :  previous_questions, 'quiz_category': quiz_category}, headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()