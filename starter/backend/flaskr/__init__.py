import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Create APP and settings cors headers
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Paginate method
    def paginate_questions(request, questions):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in questions]
        paginated_questions = questions[start:end]

        return paginated_questions

    # Questions API with pagination

    @app.route('/api/questions', methods=['GET'])
    def get_questions_with_pagination():
        error_code = 422
        try:
            categories = Category.query.all()
            questions = Question.query.all()

            formatted_questions = paginate_questions(request, questions)
            formatted_categories = [category.format()
                                    for category in categories]

            if len(formatted_categories) == 0 or len(formatted_questions) == 0:
                error_code = 404
                abort(error_code)

            current_categories = []
            for question in formatted_questions:
                category = question['category']
                if not (category in current_categories):
                    current_categories.append(category)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'current_category': current_categories,
                'categories': formatted_categories
            })
        except:
            abort(error_code)

    # Categories API

    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = [category.format()
                                    for category in categories]
            if len(formatted_categories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': formatted_categories,
                'total_categories': len(formatted_categories)
            })
        except:
            abort(422)

    # Delete Question API

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).first()
        if question is None:
            abort(404)
        try:
            question.delete()

            return jsonify({
                'success': True,
                'question': question_id
            })
        except:
            abort(405)

    # Create Question API

    @app.route('/api/questions/create', methods=['POST'])
    def new_question():
        try:
            body = request.get_json()

            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except:
            abort(422)

    # Get Questions by Category API

    @app.route(
        '/api/category/<int:question_category>/questions',
        methods=['GET']
        )
    def get_questions_by_categories(question_category):
        error_code = 422
        try:
            questions = Question.query.filter(
                question_category == Question.category).all()
            formatted_questions = paginate_questions(request, questions)

            if len(formatted_questions) == 0:
                error_code = 404
                abort(error_code)

            current_categories = []
            for question in formatted_questions:
                category = question['category']
                if not (category in current_categories):
                    current_categories.append(category)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_categories': current_categories,
            })
        except:
            abort(error_code)

    # Get Question by Search Term  API

    @app.route('/api/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        search = "%{}%".format(search_term.replace(" ", "\ "))
        data = Question.query.filter(Question.question.ilike(search)).all()
        formatted_questions = [question.format() for question in data]

        if len(formatted_questions) == 0:
            abort(404)
        try:
            current_categories = []
            for question in formatted_questions:
                category = question['category']
                if not (category in current_categories):
                    current_categories.append(category)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'totalQuestions': len(formatted_questions),
                'current_categories': current_categories,
                'search': search_term
            })
        except:
            abort(422)

    # Get Question to Play Quiz API

    @app.route('/api/quizzes', methods=['POST'])
    def post_quiz_questions():
        code = 422
        try:
            request_quiz = request.get_json()

            previous_questions = request_quiz.get('previous_questions')
            quiz_category = request_quiz.get('quiz_category')

            question = Question.query
            question = question.filter(~Question.id.in_(previous_questions))

            if quiz_category != 0:
                question = question.filter(Question.category == quiz_category)

            questions_random = question.order_by(func.random()).first()

            if not questions_random:
              return(jsonify({
                'success': True,
                'previous_question': len(previous_questions)
                }))

            return jsonify({
                'success': True,
                'question': questions_random.format(),
                'previous_question': previous_questions
            })
        except:
            abort(code)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    return app