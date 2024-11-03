import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from utilities import (
    log_error_to_file, 
    get_log_filename, 
    print_data, 
    check_api_available, 
    check_api_with_retries, 
    get_new_product_info, 
    get_updated_product_info, 
    get_product_to_delete
)

@patch('utilities.logging.error')
def test_log_error_to_file(mock_logging_error):
    """
    Test for logging an error to file.
    Mock logging.error to verify that it is called correctly 
    during error logging.
    """
    error = ValueError("Test error")
    log_error_to_file(error)
    mock_logging_error.assert_called_once()

def test_get_log_filename():
    """
    Test for generating log filename.
    Verify that the generated filename starts with "error_log_" 
    """
    filename = get_log_filename()
    assert filename.startswith("error_log_")

@patch('utilities.pd.DataFrame')
def test_print_data_valid(mock_dataframe):
    """
    Test for printing data with valid input.
    Mock pandas DataFrame to ensure 
    the correct data transformation and output call.
    """
    mock_dataframe.return_value = MagicMock()
    print_data([{"id": 1, "name": "Product A", "price": 20.0}])
    mock_dataframe.assert_called_once()

def test_print_data_empty():
    """
    Test for printing data with empty input.
    Verify that an appropriate message is printed when there are no products.
    """
    with patch('builtins.print') as mock_print:
        print_data([])
        mock_print.assert_called_once_with(
            'There are no products in database')

@patch('utilities.requests.get')
def test_check_api_available_success(mock_get):
    """
    Test for checking API availability - success.
    Mock requests.get to simulate a successful API response with status "up".
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "up"}
    mock_get.return_value = mock_response

    assert check_api_available() is True

@patch(
    'utilities.requests.get', 
    side_effect=RequestException("API not available"))
def test_check_api_available_failure(mock_get):
    """
    Test for checking API availability - failure.
    Simulate an API failure by raising a RequestException.
    """
    assert check_api_available() is False

@patch('utilities.check_api_available', side_effect=[False, True])
@patch('builtins.print')
def test_check_api_with_retries(mock_print, mock_check):
    """
    Test for retrying API check - success.
    Mock check_api_available to simulate retrying the API check until success.
    """
    assert check_api_with_retries() is True
    assert mock_check.call_count == 2  # Ensure that the check was retried

@patch('builtins.input', side_effect=['Product A', 'Description', '20.0'])
def test_get_new_product_info_valid(mock_input):
    """
    Test for getting new product info with valid input.
    Mock input() to simulate user input for a new product.
    """
    result = get_new_product_info()
    assert result == {
        "name": "Product A", 
        "price": 20.0, 
        "description": "Description"}

@patch('builtins.input', side_effect=['Product A', 'Description', 'invalid'])
@patch('utilities.log_error_to_file')
def test_get_new_product_info_invalid_price(mock_log_error, mock_input):
    """
    Test for getting new product info with invalid price.
    Verify that log_error_to_file is called when the 
    user inputs an invalid price.
    """
    result = get_new_product_info()
    assert result is False
    mock_log_error.assert_called_once()

@patch(
    'builtins.input', 
    side_effect=['1', 'Updated Product', 'Updated Description', '25.0'])
def test_get_updated_product_info_valid(mock_input):
    """
    Test for getting updated product info with valid input.
    Mock input() to simulate user input for updating a product.
    """
    result = get_updated_product_info()
    assert result == {
        "product_id": 1, 
        "name": "Updated Product", 
        "price": 25.0, 
        "description": "Updated Description"}

@patch('builtins.input', side_effect=['1'])
def test_get_product_to_delete_valid(mock_input):
    """
    Test for getting product to delete with valid ID.
    Mock input() to simulate user input for deleting a product.
    """
    result = get_product_to_delete()
    assert result == 1

@patch('builtins.input', side_effect=['invalid'])
@patch('utilities.log_error_to_file')
def test_get_product_to_delete_invalid(mock_log_error, mock_input):
    """
    Test for getting product to delete with invalid ID.
    Verify that log_error_to_file is called when the user inputs an invalid ID.
    """
    result = get_product_to_delete()
    assert result is False
    mock_log_error.assert_called_once()
