import unittest
import json
from unittest.mock import patch, MagicMock
from update_product.app import lambda_handler, update_product, category_exists, product_exists_in_category, is_invalid_image


class TestUpdateProduct(unittest.TestCase):

    @patch("update_product.pymysql.connect")  # Simulate database connection
    def test_lambda_handler_success(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.execute.return_value = None  # Simulate successful update
        mock_connect.return_value.cursor.return_value = mock_cursor

        event = {
            "body": json.dumps({
                "id": 1,
                "name": "New Name",
                "stock": 10,
                "price": 25.00,
                "status": "active",
                "image": "valid_image_data",
                "category_id": 2
            })
        }

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "PRODUCT_UPDATED")

    def test_lambda_handler_missing_body(self):
        event = {}  # Missing body in the event

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "MISSING_KEY")
        self.assertIn("error", body)  # Check for error message

    def test_lambda_handler_missing_fields(self):
        event = {
            "body": json.dumps({
                "name": "New Name"
            })
        }  # Missing required fields

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "MISSING_FIELDS")

    def test_lambda_handler_invalid_image(self):
        event = {
            "body": json.dumps({
                "id": 1,
                "name": "New Name",
                "stock": 10,
                "price": 25.00,
                "status": "active",
                "image": "invalid_image_data",  # Invalid image format
                "category_id": 2
            })
        }

        result = lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "INVALID_IMAGE")

    def test_lambda_handler_category_not_found(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (0,)  # Category not found
        patcher = patch("update_product.category_exists", return_value=False)
        with patcher as mock_category_exists:
            mock_connect.return_value.cursor.return_value = mock_cursor

            event = {
                "body": json.dumps({
                    "id": 1,
                    "name": "New Name",
                    "stock": 10,
                    "price": 25.00,
                    "status": "active",
                    "image": "valid_image_data",
                    "category_id": 2
                })
            }

            result = lambda_handler(event, None)
            self.assertEqual(result["statusCode"], 400)
            body = json.loads(result["body"])
            self.assertEqual(body["message"], "CATEGORY_NOT_FOUND")

    def test_lambda_handler_database_error(self):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = pymysql.Error  # Simulate DB error
        mock_connect.return_value.cursor.return_value = mock_cursor

        event = {
            "body": json.dumps({
                "id": 1,
                "name": "New Name",
                "stock": 10,
                "price": 25.00,
                "status": "active",
                "image": "valid_image_data",

