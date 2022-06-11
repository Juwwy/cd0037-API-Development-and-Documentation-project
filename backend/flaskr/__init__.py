
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
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)



    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
        return response



    """
    @TODO:
    ## Done
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/v1/categories', methods=['GET'])
    def categories():
        categ = Category.query.all()
        newPlant = [cate.format() for cate in categ]
        
        
        return jsonify({'success': True, 'categories': newPlant })

    """
    @TODO:

    ## Done
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1/questions')
    def questions():
        quests = Question.query.order_by(Question.id).all()
        #question = [quest.format() for quest in quests ]
        cates = Category.query.all()
        categ = [cate.format() for cate in cates]

        current_quest = paginate_quests(request, quests)

        if len(current_quest) == 0:
            abort(404)


        return jsonify({'success': True, 
        'questions': current_quest , 
        'categories' : categ,
        'number_of_questions': len(quests)
        })



    @app.route('/api/v1/questions/<int:question_id>', methods=['PATCH'])
    def question_patch(question_id):

        body = request.get_json()
        print(body)
        try:
            quest = Question.query.filter(Question.id == question_id).one_or_none()
            if quest is None:
                abort(404)

            if 'question' in body:
                quest.question = body.get('question')
            

            Question.update()

            return jsonify({
                'success' : True
            })
        except:
            abort(400)

    @app.route('/api/v1/questions/<int:question_id>', methods=['PUT'])
    def question_update(question_id):
        q1 = request.form.get('question')
        q2 = request.form.get('answer')
        q3 = request.form.get('category')
        q4 = request.form.get('difficulty')

        try:
            db.session.query(Question).filter(Question.id == question_id).update({
                'question' : q1,
                'answer': q2,
                'category': q3,
                'difficulty': q4
            })
            Question.update()
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
        

       



    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        quest = Question.query.filter(Question.id == question_id).first()

        try:
            Question.delete(quest)
            return jsonify({"success" : True, "message": "Deleted successfully!"})
        except:
            db.session.rollback()
        finally:
            db.session.close()


    """
    @TODO:
    ## Done 

    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/api/v1/questions', methods=['POST'])
    def create_question():
        try:
            request_data = request.get_json()
            
            question = request_data['question']
            answer = request_data['answer']
            difficulty = request_data['difficulty']
            category = request_data['category']
            quest = Question(question=question, answer=answer, difficulty=difficulty, category=category)
            Question.insert(quest)
            return jsonify({'success': True, 'message': 'created successful'})
        except Exception as error:
            db.session.rollback()
            print(error)
        finally:
            db.session.close()



    """
    @TODO:
    ## Done

    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/api/v1/questions/search', methods=['POST'])
    def search_question():
        total_quest = Question.query.all()
        request_data = request.get_json()
        searchval =request_data['searchTerm']
        print(searchval)
        result  = Question.query.filter(Question.question.ilike(f'%{searchval}%')).all()
        quest_str = [quest.format() for quest in result]
        cate = []
        cateType = []
        for res in result:
            cate.append( Category.query.filter(res.category == Category.id).first())
            

        for catg in cate:
            cateType.append(catg.type)

        print(len(cate))
        d = set(cateType)
        z = [s.format() for s in d]
        
        

        return jsonify({'success': True, 'questions' : quest_str, 'total_questions': len(total_quest), "current_category": z })

    """
    @TODO: 
    ## Done
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/api/v1/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        quest = Question.query.all()
        cate = Category.query.filter(Category.id == category_id ).first()
        questions = Question.query.filter(Question.category == cate.id).all()
        quest_str = [quest.format() for quest in questions]
        print(cate)
        print(questions)
        # result = Question.query.join(Category).filter(Question.category == Category.type).first()
        # print(result)
        # rest = Category.query.join(Question).filter(Category.id == category_id).filter(Category.type == Question.category).all()
        # print(rest)
        return jsonify({'success': True, 
        'total_questions': len(quest), 
        'questions': quest_str,
        'current_category': '{}'.format(cate.type)
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/api/v1/quizzes', methods=['POST'])
    def play_quiz():
        request_data = request.get_json()
        previous_questions = request_data['previous_questions']
        quiz_category_id = request_data['quiz_category']['id']

        if quiz_category_id is None:
            abort(422)
        
        if quiz_category_id == 0:
            question = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1).first()
        else:
            question = Question.query.filter(Question.category == int(quiz_category_id))\
                .filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1).first()

        print(question)

        return jsonify({
            'success': True,
            'question': question.format() 
        })
         

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found_error(error):
        return abort(404)

    @app.errorhandler(500)
    def server_error(error):
        return abort(422)

    return app

