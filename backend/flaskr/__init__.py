import os
import sys
from flask import Flask, request, abort, jsonify, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"*": {"origins": "*"}})
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
  # CATEGORIES - GET

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        categories = list(map(lambda x: x.format(), categories))
        return jsonify({
            'categories': categories,
        })
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
    def paginate_questions(page, questions):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = list(map(lambda x: x.format(), questions))
        return formatted_questions[start:end]

    def filter_questions_for_category(questions, category_id):
        if category_id == 0:
            return questions
        else:
            category = Category.query.get(category_id)
            if category is None:
                return abort(404)
            else:
                filtered_questions = list(
                    filter(lambda x: x.category == category_id, questions))
                return filtered_questions

    def get_questions_for_search_term(search_term):
        questions = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).order_by(Question.id).all()
        return questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        search_term = request.args.get('q', '', type=str)
        category_id = request.args.get('category', 0, type=int)
        questions = get_questions_for_search_term(search_term)
        filtered_questions = filter_questions_for_category(
            questions, category_id)
        totalQuestions = len(filtered_questions)
        paginated_questions = paginate_questions(page, filtered_questions)

        categories = Category.query.order_by(Category.id).all()
        categories = list(map(lambda x: x.format(), categories))
        current_category_id = category_id if category_id != 0 else None

        if ((len(paginated_questions) == 0) and (page != 1)):
            abort(404)

        return jsonify({
            'questions': paginated_questions,
            'total_questions': totalQuestions,
            'categories': categories,
            'current_category': current_category_id
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        try:
            question.delete()
            return Response(status=204)
        except:
            abort(500)
    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        question_data = request.get_json()
        if question_data is None:
            abort(400)
        new_question = question_data.get('question', None)
        new_answer = question_data.get('answer', None)
        new_category = question_data.get('category', None)
        int(new_category)
        new_difficulty = question_data.get('difficulty', None)
        int(new_difficulty)
        if ((not new_question) or (not new_answer) or (new_category is None) or (new_difficulty is None)):
            abort(400)
        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()
            new_question_data = {'question': question.format()}
            return make_response(jsonify(new_question_data), 201)
        except:
            print(sys.exc_info())
            abort(500)
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  # INCLUDED QUERY ARG IN /questions endpoint and updated front end
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    def get_questions_for_category_id(category_id):
        if ((category_id is None) or (category_id == 0)):
            questions = Question.query.order_by(Question.id).all()
            return questions
        else:
            questions = Question.query.filter(
                Question.category == category_id).order_by(Question.id).all()
            return questions

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_for_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            return abort(404)
        try:
            questions = get_questions_for_category_id(category_id)
            totalQuestions = len(questions)
            paginated_questions = paginate_questions(1, questions)
            return jsonify({
                'questions': paginated_questions,
                'total_questions': totalQuestions,
                'current_category': category_id
            })
        except:
            print(sys.exc_info())
            abort(500)

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

    def get_remaining_questions(questions_for_category, prev_questions):
        previous_questions_set = set(prev_questions)
        remaining_questions = list(filter(lambda x: not(
            x.id in previous_questions_set), questions_for_category))
        return remaining_questions

    def get_quiz_response(remaining_questions):
        if len(remaining_questions) == 0:
            response_data = jsonify({
                'quiz_completed': True,
                'remaining_questions': 0,
                'question': None
            })
            return response_data
        else:
            random_next_question = random.choice(remaining_questions)
            response_data = jsonify({
                'quiz_completed': False,
                'remaining_questions': len(remaining_questions) - 1,
                'question': random_next_question.format()
            })
            return response_data

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        quiz_data = request.get_json()
        if quiz_data is None:
            abort(400)
        quiz_category = quiz_data.get('quiz_category')
        prev_questions = quiz_data.get('previous_questions', [])
        if quiz_category is None:
            abort(400)
        try:
            quiz_category_id = quiz_category['id']
            questions = []
            if quiz_category_id == 0:
                questions = Question.query.all()
            else:
                questions = get_questions_for_category_id(
                    quiz_category_id)
            remaining_questions = get_remaining_questions(
                questions, prev_questions)
            quiz_response = get_quiz_response(remaining_questions)
            return make_response(quiz_response, 200)
        except:
            print(sys.exc_info())
            abort(500)
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": 404,
            "message": "Resource Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app
