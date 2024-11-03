import pytest
from unittest.mock import patch, mock_open, MagicMock
from utilities import (
    log_error_to_file,
    print_data,
    check_api_available,
    check_api_with_retries,
    get_new_product_info,
    get_updated_product_info,
    get_product_to_delete
)
import logging
import requests

# Prueba para log_error_to_file
def test_log_error_to_file():
    error_message = Exception("Test Error")
    with patch('logging.error') as mock_log:
        log_error_to_file(error_message)
        mock_log.assert_called_once_with(
            "An error occurred | Error type: Exception | Error message: Test Error"
        )

# Prueba para print_data
def test_print_data(capsys):
    products = [
        {'id': 1, 'name': 'Test Product', 'description': 'Test Description', 'price': 99.99}
    ]
    print_data(products)
    captured = capsys.readouterr()
    assert "Test Product" in captured.out
    assert "Test Description" in captured.out
    assert "99.99" in captured.out

# Prueba para check_api_available - éxito
def test_check_api_available_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"status": "up"})
        assert check_api_available() is True

# Prueba para check_api_available - error
def test_check_api_available_failure():
    with patch('requests.get', side_effect=requests.exceptions.RequestException):
        assert check_api_available() is False

# Prueba para check_api_with_retries - éxito
def test_check_api_with_retries_success():
    with patch('utilities.check_api_available', return_value=True):
        assert check_api_with_retries() is True

# Prueba para check_api_with_retries - error
def test_check_api_with_retries_failure():
    with patch('utilities.check_api_available', return_value=False):
        assert check_api_with_retries() is False

# Prueba para get_new_product_info - éxito
def test_get_new_product_info_success(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'Test Product')
    with patch('builtins.input', side_effect=['Test Product', 'Test Description', '99.99']):
        result = get_new_product_info()
        assert result == {
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99
        }

# Prueba para get_new_product_info - error de precio
def test_get_new_product_info_invalid_price(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'Test Product')
    with patch('builtins.input', side_effect=['Test Product', 'Test Description', 'invalid']):
        result = get_new_product_info()
        assert result is False

# Prueba para get_updated_product_info - éxito
def test_get_updated_product_info_success(monkeypatch):
    with patch('builtins.input', side_effect=['1', 'Updated Product', 'Updated Description', '150.00']):
        result = get_updated_product_info()
        assert result == {
            "product_id": 1,
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 150.00
        }

# Prueba para get_product_to_delete - éxito
def test_get_product_to_delete_success(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    with patch('builtins.input', side_effect=['1']):
        result = get_product_to_delete()
        assert result == 1

