from typing import List
from pymongo import MongoClient


class ProductService:

    def __init__(self):
        self.client = MongoClient('mongodb://josefelipetto:batera2020@ds123556.mlab.com:23556/tiagomongo')
        self.db = self.client.tiagomongo

    def get_products(self) -> List:
        return self.db.products
