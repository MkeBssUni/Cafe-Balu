import unittest
import json
from unittest.mock import patch
from get_category import app


mock_success_all = {
    "pathParameters": {
        "status": 0
    }
}

mock_success_active = {
    "pathParameters": {
        "status": 1
    }
}

mock_invalid_status = {
    "pathParameters": {
        "status": "invalid"
    }
}

mock_internal_error = {
    "pathParameters": {
        "status": 1
    }
}

class TestGetCategory(unittest.TestCase):
    @patch("get_category.app.get_all_categories")
    def test_get_all_categories_success(self, mock_get_all_categories):
        mock_get_all_categories.return_value = [
            {"id": 1, "name": "Snacks2", "status": 1},
            {"id": 2, "name": "Snacks", "status": 0}
        ]

        result = app.lambda_handler(mock_success_all, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORIES_FETCHED")
        self.assertIn("categories", body)
        self.assertEqual(len(body["categories"]), 2)

    @patch("get_category.app.get_all_categories")
    def test_get_active_categories_success(self, mock_get_all_categories):
        mock_get_all_categories.return_value = [
            {"id": 1, "name": "Snacks2", "status": 1},
            {"id": 2, "name": "Desserts", "status": 1}
        ]

        result = app.lambda_handler(mock_success_active, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORIES_FETCHED")
        self.assertIn("categories", body)
        self.assertEqual(len(body["categories"]), 2)

    def test_get_all_categories_invalid_status(self):
        result = app.lambda_handler(mock_invalid_status, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_STATUS")

    @patch("get_category.app.get_all_categories")
    def test_get_all_categories_internal_error(self, mock_get_all_categories):
        mock_get_all_categories.side_effect = Exception('Error')
        result = app.lambda_handler(mock_internal_error, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR")

    def test_decimal_to_float_invalid_type(self):
        with self.assertRaises(TypeError):
            app.decimal_to_float("string")

    @patch("get_category.app.get_all_categories")
    def test_get_all_categories_no_path_parameters(self, mock_get_all_categories):
        result = app.lambda_handler({}, None)
        status_code = result["statusCode"]
        print(result)
        self.assertEqual(status_code, 500)

    @patch("get_category.app.get_all_categories")
    def test_get_all_categories_empty_result(self, mock_get_all_categories):
        mock_get_all_categories.return_value = []

        result = app.lambda_handler(mock_success_all, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORIES_FETCHED")
        self.assertIn("categories", body)
        self.assertEqual(len(body["categories"]), 0)