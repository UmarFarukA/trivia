import json
import math
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # cors = CORS(app, resources={r"/*":{"origins":"*"}})
    
    

    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        result = [item.format() for item in selection]
        current_items = result[start : end]
        return current_items


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers','GET, POST, PUT, PATCH, DELETE')
        # response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials','true')
        return response

    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.order_by(Category.id).all()
        current_categories = paginate(request, categories)

        if categories is None:
            abort(404)
        else:
            category_collection = {}
            for category in current_categories:
                category_collection[category['id']] =  category['type']
            
            return jsonify(
                {
                    'categories': category_collection
                }
            )

    
    @app.route('/questions')
    def get_questions():
        # questions = Question.query.all()
        questions = Question.query.join(Category, Question.category == Category.id)
        current_questions = paginate(request, questions)

        categories = paginate(request, Category.query.all())
        

        total_questions = 0
        for q in questions:
            total_questions+=1

        category_collection = {}
        for cat in categories:
            category_collection[cat['id']] =  cat['type']
        

        if current_questions is None:
            abort(404)
        
        return jsonify(
            {
                'success' : True,
                'questions': current_questions,
                'categories' : category_collection,
                'totalQuestions' : total_questions,
                'currentCategory': 'History'
               
            }
        )
        

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question_to_delete = Question.query.filter_by(id = question_id).first()
            
            if question_to_delete is None:
                abort(404)
            
            question_to_delete.delete()
            return jsonify(
                {
                    'id': question_to_delete.id,
                    'status code' : 200
                }
            )
        except:
            abort(404)


    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        
        try:
            if 'question' in body and 'answer' in body and 'category' in body and 'difficulty' in body:
                question = body.get('question', None)
                answer = body.get('answer', None)
                category = int(body.get('category', None))
                difficulty = int(body.get('difficulty', None))
            else:
                abort(422)
            
            new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            new_question.insert()
            return jsonify(
                {
                    'success': True,
                    'message' : 'Successfully Added'
                }
            )
        except:
            abort(422)


    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()

        try:

            if 'searchTerm' in body:
                searchTerm = body.get('searchTerm', None)
            else:
                abort(400)

            questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
            current_questions = paginate(request, questions)

            if questions is None:
                abort(404)
            else:
                return jsonify(
                    {
                        'success': True,
                        'questions' : current_questions,
                        'total': len(questions)
                    }
                )
        except:
            abort(404)


    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        
        try:
            questions = Question.query.filter_by(category = category_id).all()
            currentCategory = Category.query.filter_by(id = category_id).first()
            
            if questions is None:
                abort(404)

            current_questions = paginate(request, questions)

            return jsonify(
                {
                    'questions' : current_questions,
                    'totalQuestions' : len(questions),
                    'currentCategory': currentCategory.type
                }
            )
        except:
            abort(404)

    
    @app.route('/quizzes', methods=["POST"])
    def play_quiz():

        body = request.get_json()

        try:
                        
            if 'quiz_category' in body and 'previous_questions' in body:
                quiz_category = int(body.get('quiz_category', None))
                previous_questions = body.get('previous_questions', None)
    
            else:
                abort(400)
           
            questions = Question.query.filter_by(category = quiz_category).all()
           
            if questions is None:
                abort(404)

            current_questions = paginate(request, questions)

            a = []
            b = []

            for q_id in previous_questions:
                if q_id not in current_questions:
                    a.append(q_id)
            
            for cq in current_questions:
                if cq not in previous_questions:
                    b.append(cq)
            
            result = a + b
            
            return jsonify(
                {
                    'success' : True,
                    'question' : result,
                }
            )

        except:
            abort(404)

    
    # Error Handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                'success': False,
                'message' : 'Bad Request'
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                'success': False,
                'message': 'Resource not found',
                'status code': 404
            }
        ), 404

    
    @app.errorhandler(405)
    def method_not_allow(error):
        return jsonify(
            {
                'success' : False,
                'message' : 'Method not Allow'
            }
        )
    
    @app.errorhandler(422)
    def unprocessed_request(error):
        return jsonify(
            {
                'success' : False,
                'message' : 'Unprocessed Request'
            }
        )


    return app

