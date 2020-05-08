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
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
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
    # QUESTIONS TESTS

    def test_get_paginated_questions_no_search_term(self):
        questions = Question.query.filter(
            Question.question.ilike('%{}%'.format(''))).order_by(Question.id).all()
        total_questions = len(questions)
        categories = Category.query.all()
        paginated_questions = total_questions if total_questions < 10 else 10
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), paginated_questions)
        self.assertEqual(data['total_questions'], total_questions)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), len(categories))
        self.assertEqual(data['current_category'], None)

    def test_get_paginated_questions_with_search_term(self):
        search_term = 'the'
        categories = Category.query.all()
        questions = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).order_by(Question.id).all()
        total_questions = len(questions)
        paginated_questions = total_questions if total_questions < 10 else 10
        res = self.client().get('/questions?page=1&q='+search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), paginated_questions)
        self.assertEqual(data['total_questions'], total_questions)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), len(categories))
        self.assertEqual(data['current_category'], None)

    def test_get_paginated_questions_with_search_term_and_category(self):
        search_term = 'the'
        categories = Category.query.all()
        questions = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).order_by(Question.id).all()
        category_id = 1
        filtered_questions = list(
            filter(lambda x: x.category == category_id, questions))
        total_questions = len(filtered_questions)
        paginated_questions = total_questions if total_questions < 10 else 10
        res = self.client().get('/questions?page=1&q=' +
                                search_term+'&category='+str(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), paginated_questions)
        self.assertEqual(data['total_questions'], total_questions)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), len(categories))
        self.assertEqual(data['current_category'], 1)

    def test_get_paginated_questions_with_search_term_no_results(self):
        search_term = 'sdasdlasjdoa'
        categories = Category.query.all()
        res = self.client().get('/questions?page=1&q='+search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), len(categories))
        self.assertEqual(data['current_category'], None)

    def test_get_paginated_questions_with_category_no_results(self):
        search_term = 'sdasdlasjdoa'
        category_id = 1
        categories = Category.query.all()
        res = self.client().get('/questions?page=1&q=' +
                                search_term+'&category='+str(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), len(categories))
        self.assertEqual(data['current_category'], 1)

    def test_error_category_not_found_get_paginated_questions(self):
        search_term = ''
        category_id = 100
        res = self.client().get('/questions?page=1&q=' +
                                search_term+'&category='+str(category_id))

        self.assertEqual(res.status_code, 404)

    def test_error_not_found_get_paginated_questions(self):
        res = self.client().get('/questions?page=1000')

        self.assertEqual(res.status_code, 404)

    def test_create_new_question(self):
        new_question = {
            'question': 'This is the new question',
            'answer': 'This is the answer',
            'category': 1,
            'difficulty': 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['question'],
                         new_question['question'])
        self.assertEqual(data['question']['category'],
                         new_question['category'])

    def test_error_create_new_question_missing_field(self):
        new_question = {
            'question': 'This is the new question',
            'category': 1,
            'difficulty': 1
        }
        res = self.client().post('/questions', json=new_question)

        self.assertEqual(res.status_code, 400)

    def test_delete_question(self):
        new_question = {
            'question': 'This is the new question',
            'answer': 'This is the answer',
            'category': 1,
            'difficulty': 1
        }
        new_question = Question(question=new_question['question'], answer=new_question['answer'],
                                category=new_question['category'], difficulty=new_question['difficulty'])
        new_question.insert()
        new_question_formatted = new_question.format()
        new_question_id = new_question_formatted['id']
        res = self.client().delete('/questions/' + str(new_question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question_id'], new_question_id)

    def test_error_not_found_delete_question(self):
        res = self.client().delete('/questions/50000')

        self.assertEqual(res.status_code, 404)

    def test_get_categories(self):
        categories = Category.query.all()
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), len(categories))

    def test_get_questions_for_category(self):
        category_id = 1
        total_questions = len(Question.query.filter(
            Question.category == category_id).all())
        res = self.client().get('/categories/' + str(category_id) + '/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], total_questions)
        self.assertEqual(data['current_category'], category_id)

    def test_error_not_found_questions_for_category(self):
        category_id = 300
        res = self.client().get('/categories/' + str(category_id) + '/questions')

        self.assertEqual(res.status_code, 404)

    def test_get_questions_for_quiz(self):
        category = Category.query.get(1)
        quiz_req_data = {
            'quiz_category': category.format(),
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=quiz_req_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['quiz_completed'], False)
        self.assertTrue(data['remaining_questions'])
        self.assertTrue(data['question'])

    def test_error_no_category_for_get_questions_for_quiz(self):
        quiz_req_data = {
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=quiz_req_data)

        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
