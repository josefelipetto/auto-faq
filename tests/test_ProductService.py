from ..services.ProductService import ProductService


def test_get_all_products():
    product_service = ProductService()
    products = product_service.get_products()
    assert products.estimated_document_count() > 0
