from typing import List
from pymongo import MongoClient
from .FAQService import FAQService
import os


class ProductService:

    def __init__(self):
        host = "ds123556.mlab.com:23556/tiagomongo?retryWrites=false"
        self.client = MongoClient(f"mongodb://{os.getenv('MONGO_DB_USER')}:{os.getenv('MONGO_DB_PASSWORD')}@{host}")
        self.db = self.client.tiagomongo

    def get_products(self) -> List:
        return list(self.db.products.find({}, {'_id': False}))

    def store_question(self, product_id: str, text: str, status: str):
        faq = FAQService(f"resources/models/faq-{product_id}.csv")
        answer = faq.try_answer(text)

        if answer['is_there_good_match']:
            self.__store_at_db(product_id, text, 'ANSWERED', answer['answer'])
            return dict(found=True, answer=answer['answer'])

        self.__store_at_db(product_id, text, status)

        self.__send_question_to_bx(product_id, text)

        return dict(found=False, answer="Pergunta enviada ao BX")

    def __store_at_db(self, product_id, text, status, answer='null'):
        self.db.products.find_one_and_update(
            {'id': product_id},
            # {'$push': {'questions': f"{{'text': '{text}', 'status': '{status}', 'answer': '{answer}'}}"}}
            {'$push': {'questions': dict(text=text, status=status, answer=answer)}}
        )

    def __send_question_to_bx(self, product_id, text):
        self.db.bxquestions.insert_one({
            'product_id': product_id,
            'question': text
        })
