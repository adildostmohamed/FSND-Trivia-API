# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## Documentation

# Trivia API Definition

## Questions

### Get Questions

Get questions and optionally filter for a specific search term or a specific category. Returns 10 questions per page.

#### Method

GET

#### Endpoint

`/questions`

#### URL Params

None

#### Query Params

- `page=[int]` - page of results (optional, defaults to 1)
- `q=[string]` - search term (optional, defaults to null)
- `category=[id]` - category (optional, defaults to null)

#### Data params

None

#### Success response

- Status code: `200`
- Response:

```
'questions': [
   {
      id: [id],
      question: [string],
      answer: [string],
      difficulty: [int],
      category: [int]
     }, ...],
'total_questions': [int],
'categories': [
   {
      id: [id],
      type: [string]
    }, ...],
'current_category': [id] | null
```

#### Errors

- No questions for page
  - Status code: `404`
  - Response: `{error: 404, message: 'Resource not found'}`
- Category not found
  - Status code: `404`
  - Response: `{error: 404, message: 'Resource not found'}`

#### Sample Call

`/questions?page=1&q=query&category=1`

### Create Question

Create a new question

#### Method

POST

#### Endpoint

`/questions`

#### URL Params

None

#### Query Params

None

#### Req Body Params

```
{
   question: [string],
   answer: [string],
   category: [int],
   difficulty: [int 1:5]
}
```

#### Success response

- Status code: `201`
- Response:

```
'question': {
   id: [id],
   question: [string],
   answer: [string],
   difficulty: [int],
   category: [int]
 }
```

#### Errors

- Missing request body data params
  - Status code: `400`
  - Response: `{error: 400, message: 'Bad Request'}`

#### Sample Call

POST - `/questions`
Request body:

```
{
   question: 'What is the new question?',
   answer: 'This is the answer',
   category: 1,
   difficulty: 1
}
```

Response:

- Status code: `200`
- Response:

```
   {
      question: {
         id: 1,
         question: 'What is the new question?',
         answer: 'This is the answer',
         category: 1,
         difficulty: 1
      }
    }
```

### Delete Question

Delete a question by its id

#### Method

DELETE

#### Endpoint

`/questions/<question_id>`

#### URL Params

- question_id[int] - required

#### Query Params

None

#### Req Body Params

None

#### Success response

- Status code: `204`
- Response: None

#### Errors

- Could not find question
  - Status code: `404`
  - Response: `{error: 404, message: 'Resource Not Found'}`

#### Sample Call

Delete - `/questions/1`
Request body:
None
Response:

- Status code: `204`
- Response: None

## Categories

### Get Categories

Get all categories

#### Method

GET

#### Endpoint

`/categories`

#### URL Params

None

#### Query Params

None

#### Data params

None

#### Success response

- Status code: `200`
- Response:

```
'categories': [
   {
      id: [id],
      type: [string]
    }, ...]
```

#### Errors

None

#### Sample Call

`/categories`

- Status code: `200`
- Response:

```
'categories': [
   {
      id: 1,
      type: 'Science'
   },
   {
      id: 2,
      type: 'Art'
   }
]
```

### Get Questions for Category

Get all questions for a category by category id

#### Method

GET

#### Endpoint

`/categories/<category_id>/questions`

#### URL Params

- category_id=[int]

#### Query Params

None

#### Data params

None

#### Success response

- Status code: `200`
- Response:

```
'questions': [
   {
      id: [id],
      question: [string],
      answer: [string],
      difficulty: [int],
      category: [int]
     }, ...],
'total_questions': [int],
'current_category': [id] | null
```

#### Errors

- Could not find category
  - Status code: `404`
  - Response: `{error: 404, message: 'Resource Not Found'}`

#### Sample Call

`/categories/1/questions`

- Status code: `200`
- Response:

```
'questions': [
   {
      id: 1,
      question: 'What is the new question?',
      answer: 'This is the answer',
      category: 1,
      difficulty: 1
    }
],
'total_questions': 1,
'current_category': 1
```

## Quizzes

### Get Random Quiz Question

Get a random next question for an active quiz for a given category. Returns a random question from the available questions for that category, whether the quiz should end and how many questions are remaining for that category.

#### Method

GET

#### Endpoint

`/quizzes`

#### URL Params

None

#### Query Params

None

#### Request Body Params

```
'quiz_category': [int],
'previous_questions': [[int], ...]
```

#### Success response

- Status code: `200`
- Response:

```
'question': {
   id: [id],
   question: [string],
   answer: [string],
   difficulty: [int],
   category: [int]
},
'quiz_completed': [bool],
'remaining_questions': [int]
```

#### Errors

- Quiz Category param missing
  - Status code: `400`
  - Response: `{error: 400, message: 'Bad Request'}`
- Quiz Category not found
  - Status code: `404`
  - Response: `{error: 404, message: 'Resource not found'}`

#### Sample Call

`/quizzes`
Request body:

```
'quiz_category': 1,
'previous_questions': [1,2, 5]
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
