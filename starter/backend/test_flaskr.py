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
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres',
            '123456',
            'localhost:5432',
            self.database_name)
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
    Write at least one test for each test
    for successful operation and for expected errors.
    """

    # CATEGORIES
    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_404_if_categories_doesnt_exist(self):
        res = self.client().get('http://localhost:5000/api/categorie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # QUESTIONS
    def test_get_questions_with_pagination(self):
        res = self.client().get('http://localhost:5000/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_get_question_with_invalid_page(self):
        res = self.client().get(
            'http://localhost:5000/api/questions?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # DELETE QUESTION
    def test_delete_question(self):
        res = self.client().delete('http://localhost:5000/api/questions/13')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_404_if_question_delete_doesnt_exist(self):
        res = self.client().delete('http://localhost:5000/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # CREATE QUESTION
    def test_post_new_question(self):
        res = self.client().post(
            'http://localhost:5000/api/questions/create',
            json={
                'question': 'Which team won the NBA Championship in 2002?',
                'answer': 'The Lakers',
                'category': 6,
                'difficulty': 3},
            headers={'Content-Type': 'application/json'})
        questions = Question.query.all()
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions))

    def test_422_if_new_question_is_unprocessable(self):
        res = self.client().post(
            'http://localhost:5000/api/questions/create',
            json={'question': '', 'category': 'rrr', 'difficulty': 3},
            headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # SEARCH WORD
    def test_post_search_questions_words(self):
        search = 'Which'
        res = self.client().post(
            'http://localhost:5000/api/questions/search',
            json={'searchTerm': search},
            headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['search'], search)

    def test_404_if_word_doesnt_exist_in_questions(self):
        search = 'esternocleidomastoideo'
        res = self.client().post(
            'http://localhost:5000/api/questions/search',
            json={'searchTerm': search},
            headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # QUESTION BY CATEGORY
    def test_get_questions_by_categories(self):
        res = self.client().get(
            'http://localhost:5000/api/category/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_categories'])

    def test_404_if_category_doesnt_exist(self):
        question_category = '1'
        res = self.client().get(
            'http://localhost:5000/api/category/question_category/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # QUIZ QUESTION
    def test_post_quiz_questions(self):
        res = self.client().post(
            'http://localhost:5000/api/quizzes',
            json={
                'previous_questions': [1, 2],
                'quiz_category': 5},
            headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['previous_question'])

    def test_422_if_quiz_is_unprocessable(self):
        res = self.client().post(
            'http://localhost:5000/api/quizzes',
            json={},
            headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
