from typing import Dict
from deeppavlov import train_model, configs
from deeppavlov.core.common.file import read_json
import csv


# Basic question filter for MVP purposes
def filter_question(question: str):
    return question \
        .replace("Olá", "") \
        .replace("ola", "") \
        .replace("Ola", "") \
        .replace("bom dia", "") \
        .replace("boa noite", "") \
        .replace("boa tarde", "") \
        .replace("opa", "") \
        .replace("Gente boa", "") \
        .replace("gente boa", "")


def update_faq_model(product_id, question, answer):
    with open(f"resources/models/faq-{product_id}.csv", 'a') as model:
        writer = csv.writer(model)
        writer.writerow((question, answer))


class FAQService:

    def __init__(self, data_path):
        self.dataPath = data_path
        self.faq = None

    def train_model(self):
        model_config = read_json(configs.faq.tfidf_logreg_en_faq)
        model_config["dataset_reader"]["data_path"] = self.dataPath
        model_config["dataset_reader"]["data_url"] = None
        self.faq = train_model(model_config)

    def try_answer(self, text):
        faq_response = self.__get_answer(filter_question(text))
        answer = faq_response['answer']
        good_similarities = list(filter(lambda similarity: similarity >= 0.6, faq_response['similarities']))
        return dict(answer=answer, is_there_good_match=len(good_similarities) > 0)

    def __get_answer(self, question: str) -> Dict:
        self.train_model()

        faq_object = self.faq([question])
        answer = faq_object[0][0]
        similarities = faq_object[1][0]

        return {
            'answer': answer,
            'similarities': similarities
        }
