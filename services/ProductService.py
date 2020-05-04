from typing import List, Dict
from pymongo import MongoClient
from .FAQService import FAQService


class ProductService:

    def __init__(self):
        self.client = MongoClient('mongodb://josefelipetto:batera2020@ds123556.mlab.com:23556/tiagomongo?retryWrites'
                                  '=false')
        self.db = self.client.tiagomongo

    def get_products(self) -> List:
        return list(self.db.products.find())

    def store_question(self, product_id: str, text: str, status: str):
        self.store_at_db(product_id, text, status)

        faq = FAQService(f"resources/models/faq-{product_id}.csv")
        answer = faq.try_answer(text)

        if answer['is_there_good_match']:
            return dict(found=True, answer=answer['answer'])

        self.send_question_to_bx(product_id, text)

        return dict(found=False, answer="Pergunta enviada ao BX")

    def store_at_db(self, product_id, text, status):
        self.db.products.find_one_and_update(
            {'id': product_id},
            {'$push': {'questions': f"{{text: \"{text}\", status: \"{status}\", answer: \"null\"}}"}}
        )

    def send_question_to_bx(self, product_id, text):
        self.db.bxquestions.insert_one({
            'product_id': product_id,
            'question': text
        })
