from requests.exceptions import RequestException

import requests

from utilities import (
    log_error_to_file, 
    APIClientError, 
    get_log_filename, 
    URL)

import requests
from requests.exceptions import RequestException
from utilities import log_error_to_file

URL = 'http://127.0.0.1:5000'

def create_product(new_product: dict) -> None:
    """Prompts the user for product info and creates it in the API."""

    try:
        # Enviar el producto a la API para ser creado
        response = requests.post(f'{URL}/products', json=new_product)
        response.raise_for_status()
        print(f"Product '{new_product['name']}' added successfully.")
    except RequestException as e:
        log_error_to_file(e)
        print(
        '''Error creating product in the API. Check the log file for details.''')


def get_products() -> list:
    """Fetches all products from the API and prints them."""
    try:
        response = requests.get(f'{URL}/products')
        response.raise_for_status()
        products = response.json()
        return products
    except RequestException as e:
        log_error_to_file(e)
        print(
            '''Error fetching products from the API. 
            Check the log file for details.''')
        return False


def update_product(product_to_update: dict) -> None:
    """Updates an existing product in the API."""
    try:
        response = requests.put(
            f"{URL}/products/{product_to_update['product_id']}",
              json=product_to_update)
        response.raise_for_status()
        print(f"Product '{product_to_update['name']}' updated successfully.")
    except RequestException as e:
        log_error_to_file(e)
        print("Error updating product in the API. Check the log file for details.")

def delete_product(product_id: int) -> None:
    """Deletes a product from the API."""
    try:
        response = requests.delete(f"{URL}/products/{product_id}")
        response.raise_for_status()
        print(f"Product with ID {product_id} deleted successfully.")
    except RequestException as e:
        log_error_to_file(e)
        print("Error deleting product in the API. Check the log file for details.")
