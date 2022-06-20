import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from sqlalchemy import JSON, func

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_quests(request, quests):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [quest.format() for quest in quests]
    current_page = questions[start:end]

   

    return current_page

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    #load_dotenv()
    setup_db(app)


    """
    @TODO: Set up CORS. Allow '*' for origins.
    """
    # ==== CORS config =========
    CORS(app, resources={r"/api/v1/*":{"origins": "*"}})



    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    #========= CORS Headers ======
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
        return response



    """
    @TODO:
    # Get all Categories
    """
    #========= Category GET Endpoint =============

    @app.route('/api/v1/categories/', methods=['GET'])
    def categories():
       try:
        categ = Category.query.all()
        newPlant = [cate.format() for cate in categ]
        return jsonify({'success': True, 'categories': newPlant })
       except:
        abort(404)

    """
    @TODO:

    ## Get all Question base on Pagination
    """

    # ========= Questions GET Endpoint ================
    @app.route('/api/v1/questions', methods=['GET'])
    def questions():
        try:
            quests = Question.query.order_by(Question.id).all()
       
            current_quest = paginate_quests(request, quests)

            if len(current_quest) == 0:
                abort(400)
            else:
                cates = Category.query.all()
                categ = [cate.format() for cate in cates]


            return jsonify({'success': True, 
            'questions': current_quest , 
            'categories' : categ,
            'number_of_questions': len(quests)
            })
        except:
            abort(404)


    #============ Question Update Endpoint ==========
    # @app.route('/api/v1/questions/<int:question_id>/update', methods=['PUT'])
    # def question_update(question_id):
    #     request_data = request.get_json()
    #     q1 = request_data['question'] 
    #     q2 = request_data['answer'] 
    #     q3 = request_data['category'] 
    #     q4 = request_data['difficulty'] 

    #     try:
    #         db.session.query(Question).filter(Question.id == question_id).update({
    #             'question' : q1,
    #             'answer': q2,
    #             'category': q3,
    #             'difficulty': q4
    #         })
           
            
    #         Question.update()
    #         return jsonify({
    #             'success': True,
    #             "message": "Update was successful!"
    #         })
    #     except Exception as error:
    #         db.session.rollback()
    #         print(error)
    #         abort(404)
    #     finally:
    #         db.session.close()
   


    """
    @TODO:
    # Delete Question
    """
    # ======== Question Delete Endpoint ==========
    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        quest = Question.query.filter(Question.id == question_id).first()

        try:
            Question.delete(quest)
            return jsonify({"success" : True,
             "message": "Deleted successfully!", 
             "id": question_id
             })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()


    """
    @TODO:
    ## Create New Question
    """
    # ======== Question Create Endpoint ============
    @app.route('/api/v1/questions', methods=['POST'])
    def create_question():
        try:
            request_data = request.get_json()

            if request_data is not None:
                question = request_data['question']
                answer = request_data['answer']
                difficulty = request_data['difficulty']
                category = request_data['category']

                quest = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                Question.insert(quest)
                return jsonify({'success': True, 'response': 201, 'message': 'created successful'})
        except Exception as error:
            db.session.rollback()
            abort(400)
        finally:
            db.session.close()



    """
    @TODO:
    ## Search
    """
    # ========= Question Search Endpoint ================
    @app.route('/api/v1/questions/search', methods=['POST'])
    def search_question():
        try:
            total_quest = Question.query.all()
            request_data = request.get_json()
            searchval = request_data['searchTerm']
            result = Question.query.filter(Question.question.ilike(f'%{searchval}%')).all()
            if len(result) > 0:
                quest_str = [quest.format() for quest in result]
                cate = []
                cateType = []
                for res in result:
                    cate.append(Category.query.filter(res.category == Category.id).first())
                for catg in cate:
                    cateType.append(catg.type)
                d = set(cateType)
                z = [s.format() for s in d]
                return jsonify({
                    'success': True,
                    'questions': quest_str,
                    'total_questions': len(total_quest),
                    "current_category": z, })
            else:
                abort(404)    
        except:
            abort(404)

    """
    @TODO: 
    # Question By Category
    """
    # ======= Get Question By Categories GET Endpoint ========
    @app.route('/api/v1/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        try:
            quest = Question.query.all()
            cate = Category.query.filter(Category.id == category_id ).first()
            questions = Question.query.filter(Question.category == cate.id).all()
            quest_str = [quest.format() for quest in questions]
            
            return jsonify({'success': True, 
            'total_questions': len(quest), 
            'questions': quest_str,
            'current_category': '{}'.format(cate.type)
            })
        except:
            return abort(404)

    """
    @TODO:

    Quiz Play
    """
    # =========== Quiz Play POST Endpoint ==========
    @app.route('/api/v1/quizzes', methods=['POST'])
    def play_quiz():
        try:
            request_data = request.get_json()
            previous_questions = request_data['previous_questions']
            quiz_category_id = request_data['quiz_category']['id']
            print(previous_questions)
            print(quiz_category_id)
            if quiz_category_id is None:
                abort(422)
            
            if quiz_category_id == 0:
                question = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1).first()
            else:
                question = Question.query.filter(Question.category == int(quiz_category_id))\
                    .filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1).first()

            #print(question.format())

            return jsonify({
                'success': True,
                'question': question.format() 
            })
        except:
            abort(422)
         

    """
    @TODO Errror Handling
    """
    # ============= Error Handling Session ==================
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success' : False,
            'error' : error,
            'message': 'Bad Request'

        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success' : False,
            'error' : 404,
            'message': 'Not found'

        }), 404

    @app.errorhandler(422)
    def server_process_error(error):
        return jsonify({
            'success' : False,
            'error' : 422,
            'message': 'Unable to process this command'

        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success' : False,
            'error' : 500,
            'message': 'Oops! your request can\'t be processed. Internal server error'

        }), 500

    #app.register_error_handler(400, bad_request_error)
    # app.register_error_handler(400, bad_request_error)
    # app.register_error_handler(422, server_process_error)
    # app.register_error_handler(404, not_found_error)
    # app.register_error_handler(500, internal_server_error)

    return app

