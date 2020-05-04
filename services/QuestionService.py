from typing import List
from pymongo import MongoClient
from .FAQService import update_faq_model
import os


class QuestionService:
    def __init__(self):
        host = "ds123556.mlab.com:23556/tiagomongo?retryWrites=false"
        self.client = MongoClient(f"mongodb://{os.getenv('MONGO_DB_USER')}:{os.getenv('MONGO_DB_PASSWORD')}@{host}")
        self.db = self.client.tiagomongo

    def get_questions(self) -> List:
        return list(self.db.bxquestions.find({}, {'_id': False}))

    def answer_question(self, product_id, question, answer):
        self.__update_product_question(product_id, question, answer)
        self.__delete_bx_question(product_id, question)
        update_faq_model(product_id, question, answer)
        return True

    def __update_product_question(self, product_id, question, answer):
        self.db.products.update(
            {
                'id': product_id,
                'questions.text': question
            },
            {
                '$set': {
                    'questions.$.answer': answer,
                    'questions.$.status': 'ANSWERED'
                }
            }
        )

    def __delete_bx_question(self, product_id, question):
        self.db.bxquestions.find_one_and_delete(
            {
                'id': product_id,
                'question': question
            }
        )
