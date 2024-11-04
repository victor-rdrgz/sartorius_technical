import pytest
from unittest.mock import patch
from main import (
    main,
    operation,
    check_api_with_retries)


import pytest
from unittest.mock import patch
from utilities import check_api_with_retries

# Test for main execution when the API becomes available
@patch('builtins.print')
@patch('main.operation')  # Patch 'operation' to avoid running actual operations
@patch('main.check_api_with_retries', return_value=True)  # Mock API check to succeed
def test_main_api_available(mock_check, mock_operation, mock_print):
    """
    Test the main execution when the API becomes available.

    Mock 'check_api_with_retries' to simulate the API being available.
    Verify that 'operation' is called.
    """
    main()
    mock_operation.assert_called_once()
    mock_print.assert_not_called()


# Test for main execution when the API is not available
@patch('builtins.print')
@patch('main.check_api_with_retries', return_value=False)  # Mock API check to fail
def test_main_api_not_available(mock_check, mock_print):
    """
    Test the main execution when the API is not available.

    Mock 'check_api_with_retries' to simulate the API being unavailable.
    Verify that the correct message is printed.
    """
    main()
    mock_print.assert_called_once_with('API is not available. Exiting program.')
    
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
def test_operation_delete_product(mock_update, mock_input):
    """
    Test the 'Update product' option in the operation function.
    Mock user input to simulate updating a product 
    and verify that update_product is called.
    """
    operation()
    mock_update.assert_called_once()
    
@patch(
    'builtins.input', 
    side_effect=['4', 'a', '0'])
@patch('main.get_product_to_delete')
def test_operation_delete_product_wrong_id(mock_delete, mock_input):
    """
    Test the 'Update product' option in the operation function.
    Mock user input to simulate updating a product with an invalid price
    (empty string). Verify that 'log_error_to_file' is called once
    when an invalid price is provided.
    """
    operation()
    mock_delete.assert_called_once()
    
@patch(
    'builtins.input', 
    side_effect=['3', '1', 'Product AA', 'Description AA','','0'])
@patch('utilities.log_error_to_file')
def test_operation_update_product_wrong_price(mock_log, mock_input):
    """
    Test the 'Update product' option in the operation function.
    Mock user input to simulate updating a product with an invalid price
    (empty string). Verify that 'log_error_to_file' is called once
    when an invalid price is provided.
    """
    operation()
    mock_log.assert_called_once()
 
@patch('builtins.input', side_effect=['a', '0'])
def test_input_in_selector_error_not_int(mock_input):
    """
    Test the selector for an incorrect input.
    Mock user input to simulate wrong value and verify 
    log_error_to_file is called.
    """
    operation()

@patch('builtins.input', side_effect=['5', '0'])
def test_input_in_selector_error_incorrect_int(mock_input):
    """
    Test the selector for an incorrect input.
    Mock user input to simulate wrong value and verify 
    log_error_to_file is called.
    """
    operation()
