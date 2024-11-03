from requests.exceptions import RequestException
import pytest
from unittest.mock import patch, MagicMock
from api_operations import (
    create_product, 
    get_products, 
    update_product, 
    delete_product
)

# Prueba para create_product - éxito
def test_create_product_success():
    new_product = {"name": "New Product", "price": 20.0, "description": "A new product"}
    with patch('requests.post') as mock_post:
        mock_post.return_value = MagicMock(status_code=201)
        create_product(new_product)
        mock_post.assert_called_once_with('http://127.0.0.1:5000/products', json=new_product)

# Prueba para create_product - error
def test_create_product_failure():
    new_product = {"name": "New Product", "price": 20.0, "description": "A new product"}
    with patch('requests.post', side_effect=RequestException("Failed to create product")), \
         patch('api_operations.log_error_to_file') as mock_log:
        create_product(new_product)
        mock_log.assert_called_once()


# Prueba para get_products - éxito
def test_get_products_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{"id": 1, "name": "Product"}])
        result = get_products()
        assert result == [{"id": 1, "name": "Product"}]

# Prueba para update_product - éxito
def test_update_product_success():
    updated_product = {"product_id": 1, "name": "Updated Product", "price": 30.0, "description": "Updated"}
    with patch('requests.put') as mock_put:
        mock_put.return_value = MagicMock(status_code=200)
        update_product(updated_product)
        mock_put.assert_called_once_with('http://127.0.0.1:5000/products/1', json=updated_product)

# Prueba para delete_product - éxito
def test_delete_product_success():
    with patch('requests.delete') as mock_delete:
        mock_delete.return_value = MagicMock(status_code=204)
        delete_product(1)
        mock_delete.assert_called_once_with('http://127.0.0.1:5000/products/1')
