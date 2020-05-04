from typing import List
from pymongo import MongoClient


class QuestionService:
    def __init__(self):
        self.client = MongoClient('mongodb://josefelipetto:batera2020@ds123556.mlab.com:23556/tiagomongo?retryWrites'
                                  '=false')
        self.db = self.client.tiagomongo

    def get_questions(self) -> List:
        return list(self.db.bxquestions.find({}, {'_id': False}))

    def answer_question(self, product_id, question, answer):
        product = self.db.products.find({'id': product_id})
        print(product.questions)

