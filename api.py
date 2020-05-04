import json
from flask import Flask, jsonify, request
from services.ProductService import ProductService
from services.QuestionService import QuestionService
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/products', methods=['GET'])
def get_products():
    product_service = ProductService()
    return jsonify(product_service.get_products())


@app.route('/question/<product_id>', methods=['POST'])
def new_question(product_id):
    text = request.json['text']
    status = 'UNANSWERED'
    product_service = ProductService()
    return jsonify(product_service.store_question(product_id, text, status))


@app.route('/bxquestions', methods=['GET'])
def get_bx_questions():
    question_service = QuestionService()
    return jsonify(question_service.get_questions())


@app.route('/answer/<product_id>', methods=['POST'])
def answer_pending_question(product_id):
    question_service = QuestionService()
    question = request.json['question']
    answer = request.json['answer']

    did_it_answer = question_service.answer_question(product_id=product_id, question=question, answer=answer)
    return jsonify(dict(success=did_it_answer))


app.run()
