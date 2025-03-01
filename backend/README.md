# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
---

`GET '/api/v1/questions'`
- Fetches a dictionary of questions in which the keys are the ids and the value is the corresponding string and integers of the questions' properties base on standard set pagination = 10 per page.
- Request Arguments: `?page=1` can be append as querystring to get content on other pages 
- Returns: An object such as the following JSON:
```json
{
  "categories": [
    {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
  ],

  "questions": 
    [{"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},
    {"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},
    {"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
    {"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
    {"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"},
    {"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"},
    {"answer":"Uruguay","category":6,"difficulty":4,"id":11,"question":"Which country won the first ever soccer World Cup in 1930?"},
    {"answer":"George Washington Carver","category":4,"difficulty":2,"id":12,"question":"Who invented Peanut Butter?"},
    {"answer":"Lake Victoria","category":3,"difficulty":2,"id":13,"question":"What is the largest lake in Africa?"},
    {"answer":"The Palace of Versailles","category":3,"difficulty":3,"id":14,"question":"In which royal palace would you find the Hall of Mirrors?"}
  ], 
  "success":true
}
```
---

`POST '/api/v1/questions'`
- Request Arguments: no request parameter needed.
- Returns: After success of the request, it generate a unique `id` for the new created object. Finally  returns an object such as the following JSON:

```json
{
  "success": true, 
  "response": 201, 
  "message": "created successful"
}
```
---


`POST '/api/v1/questions/<int:question_id>/update'`
- Request Arguments: `int:question_id` to query particular object to be updated
- Returns: An object such as the following JSON:

```json
{
  "success": true,
  "response" : 200,
  "message": "Update was successful!",
    
}
```
---

`DELETE '/api/v1/questions/<int:question_id>'`
- Request Arguments: `int:question_id` to query particular object to be deleted
- Returns: An object such as the following JSON:

```json
{
  "success" : true, 
  "response": 200,
  "id": 23,
  "message": "Deleted successfully!"
}
```
---

`POST '/api/v1/questions/search'`

- Fetches an list of dictionary of questions in which the keys are the ids and the value is the corresponding string and integers of the questions' base on the search query `searchTerm = 'title'`
- Request Arguments: no request parameter is need
- Returns: An object such as the following JSON:

```json
{
  "success": true,
  "questions": [
    {
      'id': 5, 
      'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", 
      'answer': 'Maya Angelou', 
      'category': 4, 
      'difficulty': 2
    }, 
    {
      'id': 6, 
      'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 
      'answer': 'Edward Scissorhands', 
      'category': 5, 
      'difficulty': 3
    }
    ],
  "total_questions": 23,
  "current_category": 
  [
    'Entertainment', 
    'History'
  ]
}
```
---

`GET '/api/v1/categories/<int:category_id>/questions'`
- Fetches an list of dictionary of questions in which the keys are the ids and the value is the corresponding string and integers of the questions' base on a particular category. Also, total questions count and current category base on the request made.
- Request Arguments: it fetch base on category selected. A request `'/api/v1/categories/3/questions'` will return the json below
- Returns: An object such as the following JSON:

```json
{
    "current_category": "Geography",
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "The Palace of Versailles Juwwy",
            "category": 3,
            "difficulty": 5,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 23
}
```
---
`POST '/api/v1/quizzes'`
- Fetches question at random across all categories. It work like a quiz game where total correctly answered questions score will be display at the end
- Request Arguments: no request argument needed
- Returns: An object such as the following JSON:

```json
{
  'id': 27, 
  'question': 'Who is ola of lagos', 
  'answer': 'The car spotter in Nigeria', 
  'category': 2, 
  'difficulty': 4
}
```


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
