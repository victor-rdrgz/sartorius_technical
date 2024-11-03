import pytest
from unittest.mock import patch
from main import operation

@patch(
    'builtins.input', 
    side_effect=['1', 'Test Product', 'Test Description', '20.0', '0'])
@patch('main.create_product')
def test_operation_insert_product(mock_create, mock_input):
    """
    Test the 'Insert product' option in the operation function.
    Mock user input to simulate inserting a product and 
    verify that create_product is called.
    """
    operation()
    mock_create.assert_called_once()

@patch('builtins.input', side_effect=['2', '0'])
@patch('main.get_products')
@patch('main.print_data')
def test_operation_view_products(mock_print, mock_get, mock_input):
    """
    Test the 'View all products' option in the operation function.
    Mock user input and verify that get_products and print_data are called.
    """
    mock_get.return_value = [{"id": 1, "name": "Test Product"}]
    operation()
    mock_get.assert_called()
    mock_print.assert_called()

@patch(
    'builtins.input', 
    side_effect=['3', '1', 'Updated Product',
                 'Updated Description', '25.0', '0'])
@patch('main.update_product')
def test_operation_update_product(mock_update, mock_input):
    """
    Test the 'Update product' option in the operation function.
    Mock user input to simulate updating a product 
    and verify that update_product is called.
    """
    operation()
    mock_update.assert_called_once()

@patch('builtins.input', side_effect=['4', '1', '0'])
@patch('main.delete_product')
def test_operation_delete_product(mock_delete, mock_input):
    """
    Test the 'Delete product' option in the operation function.
    Mock user input to simulate deleting a product and 
    verify that delete_product is called.
    """
    operation()
    mock_delete.assert_called_once()
