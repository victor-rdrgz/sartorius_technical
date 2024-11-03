import pytest
from unittest.mock import patch
from main import operation

# Prueba para la función operation - insertar producto
def test_operation_create_product():
    with patch('builtins.input', side_effect=['1', 'New Product', 'New Description', '20.0', '0']), \
         patch('main.create_product') as mock_create:
        operation()
        mock_create.assert_called()

# Prueba para la función operation - ver productos
def test_operation_view_products():
    with patch('builtins.input', side_effect=['2', '0']), \
         patch('main.get_products', return_value=[{"id": 1, "name": "Test Product", "price": 10.0, "description": "Test Description"}]) as mock_get, \
         patch('main.print_data') as mock_print:
        operation()
        # Verifica que `get_products()` sea llamado
        mock_get.assert_called_once()
        # Verifica que `print_data()` sea llamado con los productos
        mock_print.assert_called_once_with([{"id": 1, "name": "Test Product", "price": 10.0, "description": "Test Description"}])


# Prueba para la función operation - actualizar producto
def test_operation_update_product():
    with patch('builtins.input', side_effect=['3', '1', 'Updated Product', 'Updated Description', '50.0', '0']), \
         patch('main.update_product') as mock_update:
        operation()
        mock_update.assert_called()

# Prueba para la función operation - eliminar producto
def test_operation_delete_product():
    with patch('builtins.input', side_effect=['4', '1', '0']), \
         patch('main.delete_product') as mock_delete:
        operation()
        mock_delete.assert_called()
