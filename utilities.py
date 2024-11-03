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

# Configuración del manejador de logs para rotar cada día y eliminar 
# automáticamente archivos antiguos
log_filename = 'error_log.log'
log_handler = TimedRotatingFileHandler(
    log_filename,
    when='midnight',
    interval=1,
    backupCount=30  # Mantener archivos durante 30 días
)
log_handler.suffix = '%Y-%m-%d'  # Añadir fecha al nombre del archivo de log

# Configuración del logger
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[log_handler]
)

def log_error_to_file(error: Exception) -> None:
    '''Writes error details to a daily log file using the logging 
       module with GDPR compliance.'''
    error_message = (
        f'An error occurred | Error type: {type(error).__name__} | '
        f'Error message: {error}'
    )
    # Registrar el error
    logging.error(error_message)


# Function to get the current date-based log file name
def get_log_filename() -> str:
    '''Generate a log filename based on the current date.'''
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'error_log_{current_date}.txt'

# Custom exception
class APIClientError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

def log_error_to_file_OLD(error: Exception) -> None:
    '''Writes error details to a daily log file.'''
    log_filename = get_log_filename()
    with open(log_filename, 'a') as file:
        file.write()
        file.write('An error occurred:\n')
        file.write(f'Error type: {type(error).__name__}\n')
        file.write(f'Error message: {error}\n')
        file.write('Full traceback:\n')
        traceback.print_exc(file=file)
        file.write('\n' + '='*50 + '\n\n')

def print_data(products: list) -> None:
    '''Prints the product list in a tabular format.'''
    if not products:
        print('There are no products in database')
        return
    df_products = pd.DataFrame(products)
    df_products.set_index('id', inplace=True)
    df_products = df_products[['name', 'description', 'price']]
    print(df_products, end='\n\n')
    del df_products
    
    
def check_api_available():
    try:
        response = requests.get(f'{URL}/health')
        response.raise_for_status()
        if response.json().get('status') == 'up':
            print(f'API is available at {URL}')
            return True
    except requests.exceptions.RequestException as e:
        print(f'API is not available. Error: {e}')
    return False            
            
            
def check_api_with_retries():
    for attempt in range(MAX_RETRIES):
        if check_api_available():
            return True
        print(f'Retrying ({attempt + 1}/{MAX_RETRIES})...')
        time.sleep(RETRY_DELAY)
    print('API is not available after several attempts. Exiting program.')
    return False


def get_new_product_info() -> dict:
    
    try:
        # Solicitar el nombre del producto y verificar que no esté vacío
        name = input('Enter product name: ').strip()
        if not name:
            print('Error: Product name cannot be empty. Operation canceled.')
            return False

        # Solicitar la descripción del producto y verificar que no esté vacía
        description = input('Enter product description: ').strip()
        if not description:
            print(
                '''Error: Product description cannot be empty. 
                Operation canceled.''')
            return False
        try:
            # Solicitar el precio y convertirlo en float, 
            # verificando que sea válido
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

    except ValueError as e:
        # Controlar si el valor ingresado para el precio no es un número válido
        log_error_to_file(e)
        print('Error: Price must be a valid number. Operation canceled.')
        return False
        
        
def get_updated_product_info() -> dict:
    try:
        product_id = int(input('Enter the ID of the product to update: '))
    except ValueError as e:
        log_error_to_file(e)
        print('Error: ID must be a number. Operation canceled.')
        return False

    try:
        # Solicitar el nombre del producto y verificar que no esté vacío
        name = input('Enter product name: ').strip()
        if not name:
            print('Error: Product name cannot be empty.'
                  'Operation canceled.')
            return

        # Solicitar la descripción del producto y verificar que no esté vacía
        description = input('Enter product description: ').strip()
        if not description:
            print(
                'Error: Product description cannot be empty.Operation canceled.')
            return
        try:
            # Solicitar el precio y convertirlo en float, verificando que sea válido
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

    except ValueError as e:
        # Controlar si el valor ingresado para el precio no es un número válido
        log_error_to_file(e)
        print('Error: Price must be a valid number. Operation canceled.')
        return False

def get_product_to_delete() -> int:
    try:
        product_id = int(input('Enter the ID of the product to delete: '))
        return product_id
    except ValueError as e:
        log_error_to_file(e)
        print('Error: ID must be a number. Operation canceled.')
        return False
    