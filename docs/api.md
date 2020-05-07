# Trivia API Definition
## Questions
### Get Questions
#### Title
Get questions and optionally filter for a specific search term or a specific category
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
'questions': [{id: [id], question: [string], answer: [string], difficulty: [int], category: [int]}, ...],
'total_questions': [int],
'categories': [{id: [id], type: [string]}, ...],
'current_category': [id] | null
```
#### Errors
- Invalid page param
   - Status code: `404`
   - Response: `{error: 404, message: 'Resource not found'}`
- Invalid page param
   - Status code: `404`
   - Response: `{error: 404, message: 'Resource not found'}`
#### Sample Call
`/questions?page=1&q=query&category=1`
### Create Question
#### Title
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
'question': {id: [id], question: [string], answer: [string], difficulty: [int], category: [int]}
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
