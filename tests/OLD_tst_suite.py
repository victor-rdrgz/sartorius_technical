import unittest
from unittest.mock import patch, MagicMock
'''import api_operations
import main
import utilities'''
from project_code import api_operations, main, utilities
from requests.exceptions import RequestException


class TestUtilities(unittest.TestCase):

    @patch('utilities.datetime')
    def test_get_log_filename(self, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "2024-10-31"
        filename = utilities.get_log_filename()
        self.assertEqual(filename, "error_log_2024-10-31.txt")

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("utilities.traceback.print_exc")
    def test_log_error_to_file(self, mock_print_exc, mock_open):
        error = Exception("Test error")
        utilities.log_error_to_file(error)
        mock_open.assert_called_once_with("error_log_2024-10-31.txt", "a")
        mock_print_exc.assert_called_once()

    @patch("builtins.print")
    def test_print_data(self, mock_print):
        data = [{'id': 1, 'name': 'Product A', 'price': 10.0}]
        utilities.print_data(data)
        self.assertTrue(mock_print.called)


class TestAPIOperations(unittest.TestCase):

    @patch('api_operations.log_error_to_file')  # Correcting the patch to the actual reference
    @patch('api_operations.requests.get')
    def test_get_products_failure(self, mock_get, mock_log_error):
        # Mock a failed get_products call
        mock_get.side_effect = RequestException("API Failure")
        products = api_operations.get_products()
        self.assertIsNone(products)
        mock_log_error.assert_called_once()

    @patch('api_operations.requests.post')
    @patch("builtins.input", side_effect=["New Product", "10.0", "Description A"])
    def test_create_product_success(self, mock_input, mock_post):
        # Mock a successful create_product call
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        api_operations.create_product()
        self.assertTrue(mock_post.called)

    @patch('api_operations.log_error_to_file')
    @patch('api_operations.requests.post')
    @patch("builtins.input", side_effect=["New Product", "invalid_price", "10.0", "Description A"])
    def test_create_product_failure(self, mock_input, mock_post, mock_log_error):
        # Simulate input failure due to invalid price
        api_operations.create_product()
        mock_log_error.assert_called_once()

    @patch('api_operations.requests.put')
    @patch("builtins.input", side_effect=["y", "1", "Updated Product", "20.0", "Updated Description"])
    def test_update_product_success(self, mock_input, mock_put):
        # Mock a successful update_product call
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response

        api_operations.update_product()
        self.assertTrue(mock_put.called)

    @patch('api_operations.log_error_to_file')
    @patch('api_operations.requests.put')
    @patch("builtins.input", side_effect=["y", "invalid_id", "1", "Updated Product", "20.0", "Updated Description"])
    def test_update_product_failure(self, mock_input, mock_put, mock_log_error):
        # Simulate input failure due to invalid product ID
        api_operations.update_product()
        mock_log_error.assert_called_once()

    @patch('api_operations.requests.delete')
    @patch("builtins.input", side_effect=["y", "1"])
    def test_delete_product_success(self, mock_input, mock_delete):
        # Mock a successful delete_product call
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        api_operations.delete_product()
        self.assertTrue(mock_delete.called)

    @patch('api_operations.log_error_to_file')
    @patch('api_operations.requests.delete')
    @patch("builtins.input", side_effect=["y", "invalid_id", "1"])
    def test_delete_product_failure(self, mock_input, mock_delete, mock_log_error):
        # Simulate input failure due to invalid product ID
        api_operations.delete_product()
        mock_log_error.assert_called_once()


class TestMain(unittest.TestCase):

    @patch('main.create_product')
    @patch('builtins.input', side_effect=['1', '0'])
    def test_main_menu_create_product(self, mock_input, mock_create_product):
        mock_create_product.return_value = None
        with patch('builtins.print'):
            main.operation()
        self.assertTrue(mock_create_product.called)

    @patch('main.get_products')
    @patch('builtins.input', side_effect=['2', '0'])
    def test_main_menu_view_products(self, mock_input, mock_get_products):
        mock_get_products.return_value = [{'id': 1, 'name': 'Product A'}]
        with patch('builtins.print'):
            main.operation()
        self.assertTrue(mock_get_products.called)

    @patch('main.update_product')
    @patch('builtins.input', side_effect=['3', '0'])
    def test_main_menu_update_product(self, mock_input, mock_update_product):
        mock_update_product.return_value = None
        with patch('builtins.print'):
            main.operation()
        self.assertTrue(mock_update_product.called)

    @patch('main.delete_product')
    @patch('builtins.input', side_effect=['4', '0'])
    def test_main_menu_delete_product(self, mock_input, mock_delete_product):
        mock_delete_product.return_value = None
        with patch('builtins.print'):
            main.operation()
        self.assertTrue(mock_delete_product.called)


if __name__ == '__main__':
    unittest.main()
