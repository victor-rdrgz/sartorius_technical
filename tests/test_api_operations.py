import pytest
from unittest.mock import patch, MagicMock
from api_operations import (
    create_product, 
    get_products, 
    update_product, 
    delete_product
)
from requests.exceptions import RequestException

@patch('api_operations.requests.post')
def test_create_product_success(mock_post):
    """
    Test for create_product - success.
    Mock requests.post to simulate a successful creation of a product.
    """
    new_product = {
        "name": "New Product", 
        "price": 20.0, 
        "description": "A new product"}
    mock_post.return_value = MagicMock(status_code=201)
    create_product(new_product)
    mock_post.assert_called_once_with(
        'http://127.0.0.1:5000/products', 
        json=new_product)

@patch('api_operations.requests.post', side_effect=RequestException("Failed to create product"))
@patch('api_operations.log_error_to_file')
def test_create_product_failure(mock_log, mock_post):
    """
    Test for create_product - failure.
    Simulate a failed product creation by raising a RequestException.
    """
    new_product = {
        "name": "New Product", 
        "price": 20.0, 
        "description": "A new product"}
    create_product(new_product)
    mock_log.assert_called_once()

@patch('api_operations.requests.get')
def test_get_products_success(mock_get):
    """
    Test for get_products - success.
    Mock requests.get to simulate successfully fetching product data.
    """
    mock_get.return_value = MagicMock(
        status_code=200, 
        json=lambda: [{"id": 1, "name": "Product 1"}])
    
    products = get_products()
    assert products == [{"id": 1, "name": "Product 1"}]
    mock_get.assert_called_once_with('http://127.0.0.1:5000/products')

@patch('api_operations.requests.get', side_effect=RequestException("Failed to get products"))
@patch('api_operations.log_error_to_file')
def test_get_products_failure(mock_log, mock_get):
    """
    Test for get_products - failure.
    Simulate an API failure by raising a RequestException.
    """
    products = get_products()
    assert products is False
    mock_log.assert_called_once()

@patch('api_operations.requests.put')
def test_update_product_success(mock_put):
    """
    Test for update_product - success.
    Mock requests.put to simulate a successful product update.
    """
    updated_product = {
        "product_id": 1, 
        "name": "Updated Product", 
        "price": 25.0, 
        "description": "Updated description"}
    mock_put.return_value = MagicMock(status_code=200)
    update_product(updated_product)
    mock_put.assert_called_once_with(
        'http://127.0.0.1:5000/products/1', 
        json=updated_product)

@patch('api_operations.requests.put', side_effect=RequestException("Failed to update product"))
@patch('api_operations.log_error_to_file')
def test_update_product_failure(mock_log, mock_put):
    """
    Test for update_product - failure.
    Simulate a failed product update by raising a RequestException.
    """
    updated_product = {
        "product_id": 1, 
        "name": "Updated Product", 
        "price": 25.0, 
        "description": "Updated description"}
    update_product(updated_product)
    mock_log.assert_called_once()

@patch('api_operations.requests.delete')
def test_delete_product_success(mock_delete):
    """
    Test for delete_product - success.
    Mock requests.delete to simulate a successful product deletion.
    """
    mock_delete.return_value = MagicMock(status_code=204)
    delete_product(1)
    mock_delete.assert_called_once_with(
        'http://127.0.0.1:5000/products/1')

@patch('api_operations.requests.delete', side_effect=RequestException("Failed to delete product"))
@patch('api_operations.log_error_to_file')
def test_delete_product_failure(mock_log, mock_delete):
    """
    Test for delete_product - failure.
    Simulate a failed product deletion by raising a RequestException.
    """
    delete_product(1)
    mock_log.assert_called_once()
