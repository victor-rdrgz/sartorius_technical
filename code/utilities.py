import traceback
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

import requests
import pandas as pd

# Constants
URL = 'http://127.0.0.1:5000'
MAX_RETRIES = 5
RETRY_DELAY = 3

# Configuration for rotating logs daily and automatically deleting old files
log_filename = 'error_log.log'
log_handler = TimedRotatingFileHandler(
    log_filename,
    when='midnight',
    interval=1,
    backupCount=30  # Keep log files for 30 days
)
log_handler.suffix = '%Y-%m-%d'  # Append date to the log file name

# Logger configuration
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[log_handler]
)

def log_error_to_file(error: Exception) -> None:
    """
    Log error details to a daily log file using the logging module.

    Args:
        error (Exception): The error to log.

    This function will generate an error message with the error type and 
    message, and log it to the file.
    """
    error_message = (
        f'An error occurred | Error type: {type(error).__name__} | '
        f'Error message: {error}'
    )
    # Log the error
    logging.error(error_message)


def get_log_filename() -> str:
    """
    Generate a log filename based on the current date.

    Returns:
        str: The log file name including the current date.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'error_log_{current_date}.txt'

# Custom exception
class APIClientError(Exception):
    """
    Custom exception class for API client errors.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def print_data(products: list) -> None:
    """
    Print the product list in a tabular format.

    Args:
        products (list): The list of products to be printed.

    Converts the list of products to a DataFrame and prints it in a structured 
    format. If the product list is empty, it prints an informative message.
    """
    if not products:
        print('There are no products in database')
        return
    df_products = pd.DataFrame(products)
    df_products.set_index('id', inplace=True)
    df_products = df_products[['name', 'description', 'price']]
    print(df_products, end='\n\n')
    del df_products


def check_api_available() -> bool:
    """
    Check if the API is available.

    Returns:
        bool: True if the API is available, False otherwise.

    Attempts to perform a health check on the API. If the API is up, prints a 
    success message; otherwise, prints the error message.
    """
    try:
        response = requests.get(f'{URL}/health')
        response.raise_for_status()
        if response.json().get('status') == 'up':
            print(f'API is available at {URL}')
            return True
    except requests.exceptions.RequestException as e:
        print(f'API is not available. Error: {e}')
    return False


def check_api_with_retries() -> bool:
    """
    Retry API availability check multiple times.

    Returns:
        bool: True if the API becomes available, False if all retries fail.

    This function will retry checking the API availability up to MAX_RETRIES 
    times with a delay between each retry.
    """
    for attempt in range(MAX_RETRIES):
        if check_api_available():
            return True
        print(f'Retrying ({attempt + 1}/{MAX_RETRIES})...')
        time.sleep(RETRY_DELAY)
    print('API is not available after several attempts. Exiting program.')
    return False


def get_new_product_info() -> dict:
    """
    Get the information for creating a new product from user input.

    Returns:
        dict: Dictionary containing product details if input is valid.
        Returns False if any input is invalid.

    Prompts the user for product name, description, and price, and returns the 
    information as a dictionary. If the input is invalid (e.g., empty fields 
    or non-numeric price), logs the error and prints an error message.
    """
    # Request product name and ensure it is not empty
    name = input('Enter product name: ').strip()
    if not name:
        print('Error: Product name cannot be empty. Operation canceled.')
        return False

    # Request product description and ensure it is not empty
    description = input('Enter product description: ').strip()
    if not description:
        print('Error: Product description cannot be empty.'
                'Operation canceled.')
        return False

    # Request product price and convert it to float, validating input
    try:
        price = float(input('Enter product price: '))
    except ValueError as e:
        log_error_to_file(e)
        print('Error: Price must be a number. Operation canceled.')
        return False

    new_product = {
        'name': name,
        'price': price,
        'description': description
    }
    return new_product

def get_updated_product_info() -> dict:
    """
    Get information for updating an existing product from user input.

    Returns:
        dict: Dictionary containing updated product details if input is valid.
        Returns False if any input is invalid.

    Prompts the user for the product ID, name, description, and price to update
    an existing product. Logs errors for invalid input and 
    prints corresponding messages.
    """
    try:
        product_id = int(input('Enter the ID of the product to update: '))
    except ValueError as e:
        log_error_to_file(e)
        print('Error: ID must be a number. Operation canceled.')
        return False

    # Request product name and ensure it is not empty
    name = input('Enter product name: ').strip()
    if not name:
        print('Error: Product name cannot be empty. Operation canceled.')
        log_error_to_file(
            'Error: Product name cannot be empty. Operation canceled.')
        return False

    # Request product description and ensure it is not empty
    description = input('Enter product description: ').strip()
    if not description:
        log_error_to_file(
            'Error: Product name cannot be empty. Operation canceled.')
        print('Error: Product description cannot be empty.'
                'Operation canceled.')
        return False

    # Request product price and convert it to float, validating input
    try:
        price = float(input('Enter product price: '))
    except ValueError as e:
        log_error_to_file(e)
        print('Error: Price must be a number. Operation canceled.')
        return False

    updated_product = {
        'product_id': product_id,
        'name': name,
        'price': price,
        'description': description
    }
    return updated_product

def get_product_to_delete() -> int:
    """
    Get the ID of the product to delete.

    Returns:
        int: The ID of the product to delete if input is valid.
        Returns False if the input is invalid.

    Prompts the user for the product ID and logs errors for invalid input.
    """
    try:
        product_id = int(input('Enter the ID of the product to delete: '))
        return product_id
    except ValueError as e:
        log_error_to_file(e)
        print('Error: ID must be a number. Operation canceled.')
        return False
