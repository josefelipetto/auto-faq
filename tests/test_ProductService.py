from unittest import TestCase

from ..services.ProductService import ProductService


def test_get_all_products():
    product_service = ProductService()
    products = product_service.get_products()
    assert len(products) > 0


def test_store_new_question():
    product_service = ProductService()
    response = product_service.store_question(product_id="MLB1353146627",
                                              text="Boa tarde parceiro, quais são as medidas dela?",
                                              status="A")

    assert response.get('found') is not None
    assert response.get('found')
