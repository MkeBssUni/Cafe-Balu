import unittest
import json
from unittest.mock import patch, MagicMock
from save_sale.app import lambda_handler, get_products_info

class TestSaveSale(unittest.TestCase):

    @patch("save_sale.pymysql.connect")  # Simulate database connection
    def test_lambda_handler_success(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = [None, None, None]  # Simulate successful executions
        mock_connect.return_value.cursor.return_value = mock_cursor

        event = {
            "body": json.dumps({
                "products": [
                    {"id": 1, "quantity": 2}
                ],
                "total": 25.00
            })
        }

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "SALE_SAVED")
        self.assertTrue("sale_id" in body)  # Verify sale_id is included

    # ... (Add more test cases to cover different scenarios) ...

    def test_lambda_handler_missing_body(self):
        event = {}  # Missing body in the event

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "BAD_REQUEST")
        self.assertIn("error", body)  # Check for error message

    def test_lambda_handler_missing_products(self):
        event = {
            "body": json.dumps({
                "total": 25.00
            })
        }  # Missing products field

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "BAD_REQUEST")
        self.assertIn("error", body)  # Check for error message

    def test_lambda_handler_missing_total(self):
        event = {
            "body": json.dumps({
                "products": [
                    {"id": 1, "quantity": 2}
                ]
            })
        }  # Missing total field

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "BAD_REQUEST")
        self.assertIn("error", body)  # Check for error message

    def test_get_products_info_invalid_quantity(self):
        products = [{"id": 1, "quantity": 0}]  # Invalid product quantity

        with self.assertRaises(ValueError) as e:
            get_products_info(products)
        self.assertEqual(str(e.exception), "Product with id 1 has invalid quantity")

    def test_save_sale_database_error(self, mock_connect=None, pymysql=None):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = [None, None, pymysql.Error]  # Simulate DB error
        mock_connect.return_value.cursor.return_value = mock_cursor

        event = {
            "body": json.dumps({
                "products": [
                    {"id": 1, "quantity": 2}
                ],
                "total": 25.00
            })
        }

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 500)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "DATABASE_ERROR")
        self.assertIn("error", body)  # Check for error message

if __name__ == "__main__":
    unittest.main()
