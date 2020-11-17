import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in questions]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories', methods=['GET'])
  def get_categories():
    try:
      categories = Category.query.all()
      formatted_categories = [category.format() for category in categories]
      if len(formatted_categories) == 0:
        abort(404)

      return jsonify({
        'success': True,
        'categories': formatted_categories,
        'total_categories': len(formatted_categories)
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions', methods=['GET'])
  def get_questions():
    try:
      page = request.args.get('page', 1, type=int)
      start = (page -1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      categories = Category.query.all()
      questions = Question.query.all()
      formatted_questions = [question.format() for question in questions]
      formatted_categories = [category.format() for category in categories]
      if len(formatted_categories) == 0 or len(formatted_questions) == 0:
        abort(404)
      
      current_categories = []
      for question in formatted_questions:
        category = question['category']
        if not (category in current_categories):
          current_categories.append(category)

      return jsonify({
        'success': True,
        'list_questions': formatted_questions[start:end],
        'number_total_questions': len(formatted_questions),
        'current_category': current_categories,
        'categories': formatted_categories[start:end]
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
      abort(404)
    try:
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'question': question_id,
        'questions': current_questions,
        'total_question': len(Question.query.all())
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions/create', methods=['POST'])
  def new_question():
    try:
      body = request.get_json()
      
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)

      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id
      })

    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    search = "%{}%".format(search_term.replace(" ", "\ "))
    data = Question.query.filter(Question.question.ilike(search)).all()
    formatted_questions = [q.format() for q in data]

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
        'currentCategories': current_categories,
        'search': search
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/questions/<string:question_category>', methods=['GET'])
  def get_questions_by_categories(question_category):
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.join(Category, Question.category == Category.id).filter(Category.type.ilike(question_category)).all()
    formatted_questions = [question.format() for question in questions]

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
        'questions': formatted_questions[start:end],
        'total_question': len(formatted_questions),
        'currentCategories': current_categories,
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/quizzes', methods=['POST'])
  def post_quiz_questions():
    try:
      request_quiz = request.get_json()

      previous_questions = request_quiz.get('previous_questions', None)
      quiz_category = request_quiz.get('quiz_category', None)

      questions_random = Question.query.filter(Question.category == quiz_category).filter(~Question.id.in_(previous_questions)).order_by(func.random()).first()

      return jsonify({
        'success': True,
        'question': questions_random.format(),
        'previous_question': previous_questions
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
    }), 500
  
  @app.route('/')
  def index():
    return jsonify({'message':'hola mortales'})
  
  return app

    