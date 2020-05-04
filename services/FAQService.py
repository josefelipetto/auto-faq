from typing import Dict
from deeppavlov import train_model, configs
from deeppavlov.core.common.file import read_json


class FAQService:

    def __init__(self, data_path):
        self.dataPath = data_path
        self.faq = None

    def train_model(self):
        model_config = read_json(configs.faq.tfidf_logreg_en_faq)
        model_config["dataset_reader"]["data_path"] = self.dataPath
        model_config["dataset_reader"]["data_url"] = None
        self.faq = train_model(model_config)

    def get_answer(self, question: str) -> Dict:
        self.train_model()

        faq_object = self.faq([question])
        answer = faq_object[0][0]
        similarities = faq_object[1][0]

        return {
            'answer': answer,
            'similarities': similarities
        }

    def try_answer(self, text):
        faq_response = self.get_answer(text)
        answer = faq_response['answer']
        good_similarities = list(filter(lambda similarity: similarity > 0.6, faq_response['similarities']))
        return dict(answer=answer, is_there_good_match=len(good_similarities) > 0)
