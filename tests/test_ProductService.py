from unittest import TestCase

from ..services.ProductService import ProductService


def test_get_all_products():
    product_service = ProductService()
    products = product_service.get_products()
    assert len(products) > 0


def test_store_new_question():
    product_service = ProductService()
    product_service.store_question(product_id="MLB1353146627", text="Teste Question", status="A")
