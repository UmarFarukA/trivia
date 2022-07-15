## Introduction

- This Trivia app provides users with the ability to answer questions (quizzez) and add new questions according to category such whather they belong to sports, entertainment, science, etc. Users can choose the category of questions they wish to answer.

### Getting Started

- Base URL: At present, the application can only be access locally via 127.0.0.1:3000.
- API keys or Authentication: Neither an API key or authentication is required to access the application via the mentioned URL.

### Error Handling

- The application return errors in json format upon a fail request as shown below
  {
  "message": "Resource not found",
  "success": false
  }
- Similarly, the API will handle and return these forms of errors:
  - 400: Bad Request
  - 404: Resource Not Found
  - 405: Method not allow
  - 422: Not Processable

### Endpoints

#### GET /questions

- Gemeral:

  - This endpoint returns the list of questions, all available categories, total number of questions and the current category. The result is paginated to questions per page.
  - Sample: curl http://127.0.0.1:5000/questions
    '{
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    },
    "questions": [
    {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
    },
    {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
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
    },
    {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
    },
    {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
    },
    {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
    }
    ],
    "totalQuestions": 19
    }'

#### GET /categories

- General: This endpoint return all categories available in the app.
- Sample: curl http://127.0.0.1:5000/categories

  ```
  {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
  }
  ```

#### DELETE /questions/{questions_id}

- General: This endpoint delete a question based on it Id. It returns the ID of the deleted questions and the status code of the request.
- Sample: curl -X DELETE http://127.0.0.1:5000/questions/25
  ```
  {
  "id": 25,
  "status code": 200
  }
  ```

#### POST /questions

- General: The endpoint create a new question by taking request parameters such the question, answer, category and the difficulty score. Upon successful submission it returns the success value and a message.

- Sample: curl -X POST -H "Content-Type: application/json" -d '{"question":"Which dung beetle was worshipped by the ancient Egyptians?","answer":"Scarab","category":4,"difficulty":4}' http://127.0.0.1:5000/questions

  {
  "message": "Successfully Added",
  "success": true
  }

#### POST /questions/search

- General: Similar to the above endpoint of creating questions, this endpoint takes single parameter request, search term, which is used to search for any question with given search term. It returns a success value, list of all question containing the search term and the total questions.
- Sample: curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"What actor did author"}' http://127.0.0.1:5000/questions/search

```
{
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total": 1
}
```

#### GET /categories/{category_id}/questions

- General: This endpoint returns list of questions based on the category ID, the success value, total questions and the current category.
- Sample: curl http://127.0.0.1:5000/categories/6/questions

```
{
  "currentCategory": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "totalQuestions": 2
}
```

#### POST /quizzes

- General: This endpoint returns the success value and the questions by taking the quiz category and the previous questions;
  -Sample: curl -X POST -H "Content-Type: application/json" -d '{"quiz_category":5, "previous_questions":[]}' http://localhost:5000/quizzes

  '' '
  {
  "question": [
  [
  {
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4,
  "id": 2,
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
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
  ]
  ],
  "success": true
  }
  '''
