# Trivia API Definition
## Questions

#### Title
Get questions and optionally filter for a specific search term or a specific category
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
