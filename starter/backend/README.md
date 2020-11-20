# Full Stack Trivia API Backend 🐱‍💻

This project is a **Virtual Trivia** that I do myself for **Udacity**. In this you can add questions, give them answers, category and difficulty, delete questions and play with the questions of the questionnaire guessing the answer. As part of the Fullstack Nanodegree, this serves as practice for **Course 2: API Development and Documentation**. In this project, I applied API endpoint structuring, implementation, and formatting with knowledge of HTTP and APi development best practices.

**Ready to run it, Let's get started 🤓**
 
## Getting Started 🚀

### Installing Dependencies
#### Python 3.7 🐍

Follow instructions to install the latest version of python for your platform in the  [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### [](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter/backend#virtual-enviornment)Virtual Enviornment 💻

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the  [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### [](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter/backend#pip-dependencies)PIP Dependencies 🐱‍🐉

Once you have your virtual environment setup and running, install dependencies by naviging to the  `/backend`  directory and running:

pip install -r requirements.txt

This will install all of the required packages we selected within the  `requirements.txt`  file.

##### [](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter/backend#key-dependencies)Key Dependencies 💾

-   [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
    
-   [SQLAlchemy](https://www.sqlalchemy.org/)  is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
    
-   [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)  is the extension we'll use to handle cross origin requests from our frontend server.
The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## Database Setup 🗄

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

psql trivia < trivia.psql

## [](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter/backend#running-the-server)Running the server 🏃‍♂️💻

From within the  `backend`  directory first ensure you are working using your created virtual environment.

To run the server, execute:

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

Setting the  `FLASK_ENV`  variable to  `development`  will detect file changes and restart the server automatically.

Setting the  `FLASK_APP`  variable to  `flaskr`  directs flask to use the  `flaskr`  directory and the  `__init__.py`  file to find the application.

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API Reference 📁

## Getting Started 🚀

 - Base URL: At present this app can only ru locally and is not hosted as a base URL. The backend app is hosted at default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
 - Authentication: This version of the application does not require authentication or API keys.

## Error Handling 💣

Errors are returned as JSON objects in the following format:

    {
	    "success": False,
	    "error": 404,
	    "message": "resource not found"
    }

The API return three types when request fall:

 - 400: Bad Request
 - 404: Resource Not Found
 - 422:  Unprocessable

## Endpoints 🚩

**GET /api/questions**

 - General:
	 - Get all questions with the paginated. Returns all questions categories, current_category, questions, success, total_questions.
	 -  `curl -X GET http://localhost:5000/api/questions`
  
```
{"categories": [
        { "id": 1,
          "type": "Science"
        },
        { "id": 2,
          "type": "Art"
        },
        { "id": 3,
          "type": "Geography"
        },
        { "id": 4,
          "type": "History"
        },
        { "id": 5,
          "type": "Entertainment"
        },
        { "id": 6,
          "type": "Sports"
        }
      ],
      "current_category": [4,5],
      "questions": [
	        { "answer": "Maya Angelou",
	          "category": 4,
	          "difficulty": 2,
	          "id": 5,
	          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	        },
	        { "answer": "Muhammad Ali",
	          "category": 4,
	          "difficulty": 1,
	          "id": 9,
	          "question": "What boxer's original name is Cassius Clay?"
	        },
	        { "answer": "Tom Cruise",
	          "category": 5,
	          "difficulty": 4,
	          "id": 4,
	          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
	        }
      ],
      "success": true,
      "total_questions": 3
    }
```
   
  **GET /api/categories**

 - General:
	 - Get all categories. Returns all categories, success, total_categories.
	 -  `curl -X GET http://localhost:5000/api/categories`

```
	{
	  "categories": [
			    {     "id": 1, 
				      "type": "Science"
			    }, 
			    {     "id": 2, 
				      "type": "Art"
			    }, 
			    {     "id": 3, 
				      "type": "Geography"
			    }, 
			    {      "id": 4, 
				      "type": "History"
			    }, 
			    {      "id": 5, 
				      "type": "Entertainment"
			    }, 
			    {     "id": 6, 
				      "type": "Sports"
			    }
		  ], 
		  "success": true, 
		  "total_categories": 6
	}
```

  **DELETE/api/questions/question_id**

 - General:
	 - Delete one question select by id. Returns success, question_id deleted.
	 -  `curl -X DELETE http://localhost:5000/api/questions/2`

```
{
  "question": 9,
  "success": true
}
```

   **POST/api/questions/create**

 - General:
	 - Creates a new question using question, answer, category and difficulty . Returns id of the created question, success value.
	 -  `curl -X POST -d '{answer:"Maya quizzes",category:3,difficulty:4,question:"Whose autobiography is entitled"}' -H 'Content-type:application/json' http://localhost:5000/api/questions/create`

```
{
  "created": 33,
  "success": true
}
```


   **POST/api/questions/search**

 - General:
	 - Get an array of question with the keyword determined by the searchTerm. The response have: questions, totalQuestions, current_categories and search. 
	 -  `curl -X POST -d '{"searchTerm":"What"}' -H 'Content-type:application/json' http://localhost:5000/api/questions/search`

```
{
  "current_categories": [
    5
  ],
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "search": "What",
  "success": true,
  "totalQuestions": 2
}
```

   **GET/api/category/\<question_category\>/questions**

 - General:
	 - Get the questions by category determined by the id question_category, the resutl is an array with the paginated questions. The response have: success, questions, total_questions and current_categories.
	 -  `curl -X GET http://localhost:5000/api/category/\<question_category\>/questions`

```
{
  "current_categories": [
    1
  ],
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

   **POST /api/quizzes**

 - General:
	 - Get one random question determined by the quiz_category and not in the previous_questions array. To have one without category, quiz_category need to be 0. The response have: success, question, previous_question
	 -  `curl -X POST -d '{"previous_questions":[1,2],"quiz_category":1}' -H 'Content-type:application/json' http://localhost:5000/api/quizzes`

```
{
"success": true,
"question": {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
"previous_question": [1,2]
}
```

## Authors 
Estefania Aranguren
