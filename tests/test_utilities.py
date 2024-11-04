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
    get_product_to_delete,
    APIClientError
)

def test_api_client_error():
    """
    Test for the custom exception APIClientError.
    Verify that the exception stores the message correctly.
    """
    # Define the message for the exception
    message = "This is a test error message."
    
    # Create an instance of APIClientError with the message
    exception_instance = APIClientError(message)
    
    # Assert that the message is stored correctly in the exception instance
    assert exception_instance.message == message
    assert str(exception_instance) == message  # Ensure the message is returned correctly by str()

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
    
@patch('builtins.input', side_effect=['',])
@patch('utilities.log_error_to_file')
def test_get_new_product_info_empty_name(mock_log_error, mock_input):
    """
    Test for getting new product info with invalid price.
    Verify that log_error_to_file is called when the 
    user inputs an invalid price.
    """
    result = get_new_product_info()
    assert result is False
    
@patch('builtins.input', side_effect=['Product ZZ', ''])
@patch('utilities.log_error_to_file')
def test_get_new_product_info_empty_description(mock_log_error, mock_input):
    """
    Test for getting new product info with invalid price.
    Verify that log_error_to_file is called when the 
    user inputs an invalid price.
    """
    result = get_new_product_info()
    assert result is False

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

@patch('builtins.input', side_effect=['a', 0])
@patch('utilities.log_error_to_file')
def test_get_updated_product_info_invalid_id(mock_error, mock_input):
    """
    Test for getting updated product info with valid input.
    Mock input() to simulate user input for updating a product.
    """
    result = get_updated_product_info()
    mock_error.assert_called_once()
    assert result == False
    
@patch('builtins.input', side_effect=['1',''])
@patch('utilities.log_error_to_file')
def test_get_updated_product_info_invalid_name(mock_error, mock_input):
    """
    Test for getting updated product info with valid input.
    Mock input() to simulate user input for updating a product.
    """
    result = get_updated_product_info()
    mock_error.assert_called_once()
    assert result == False
    
@patch('builtins.input', side_effect=['1','Product A', ''])
@patch('utilities.log_error_to_file')
def test_get_updated_product_info_invalid_description(mock_error, mock_input):
    """
    Test for getting updated product info with valid input.
    Mock input() to simulate user input for updating a product.
    """
    result = get_updated_product_info()
    mock_error.assert_called_once()
    assert result == False

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
    
# Test for check_api_with_retries when API becomes available
@patch('utilities.time.sleep')  # Patch sleep to avoid delays during the test
@patch('utilities.check_api_available', side_effect=[False, False, True])
def test_check_api_with_retries_success(mock_check, mock_sleep):
    """
    Test the 'check_api_with_retries' function when the API becomes available
    after a few retries.
    
    Mock 'check_api_available' to simulate the API becoming available after
    a few retries. Ensure the function returns True.
    """
    result = check_api_with_retries()
    assert result is True
    assert mock_check.call_count == 3  # Should have been called three times

# Test for check_api_with_retries when API fails to become available
@patch('utilities.time.sleep')  # Patch sleep to avoid delays during the test
@patch('utilities.check_api_available', side_effect=[False] * 5)
def test_check_api_with_retries_failure(mock_check, mock_sleep):
    """
    Test the 'check_api_with_retries' function when the API fails to become available
    after all retries.
    
    Mock 'check_api_available' to simulate the API being unavailable for all retries.
    Ensure the function returns False.
    """
    result = check_api_with_retries()
    assert result is False
    assert mock_check.call_count == 5  # Should have been called MAX_RETRIES times


