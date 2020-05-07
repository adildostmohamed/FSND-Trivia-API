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
Delete a  question by its id
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
-  category_id=[int]
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
