# -*- coding: UTF-8 -*-
import requests
import csv
import time


def generatecsv(itemid, questions):
    with open(f"generatedModels/faq-{itemid}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Question', 'Answer'))
        for question in questions:
            writer.writerow((question['text'], question['answer']['text']))


ACCESS_TOKEN = "APP_USR-8450736370994355-050120-8e8cdb6896e7731e2d1e19f85c0065a7-30762069"
BASE_API_URL = "https://api.mercadolibre.com"
OLIST_STORE_URL = "/sites/MLB/search?seller_id=219324699"
olistItensResponse = requests.get(f"{BASE_API_URL}{OLIST_STORE_URL}")

items = olistItensResponse.json()

for item in items['results']:
    itemId = item['id']
    print(f"Requesting question of item {itemId} - {item['title']}")
    questions = requests.get(
        f"{BASE_API_URL}/questions/search?item_id={itemId}&access_token={ACCESS_TOKEN}&status=ANSWERED").json()[
        'questions']
    generatecsv(itemId, questions)
    time.sleep(2)
