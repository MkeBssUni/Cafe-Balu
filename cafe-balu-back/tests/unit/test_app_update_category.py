import unittest
import json
from update_category import app
from unittest.mock import patch

mock_name_duplicated = {
    "body": json.dumps({
        "id": 1,
        "name": "Pasteles"
    })
}

mock_category_not_exists = {
    "body": json.dumps({
        "id": 1506,
        "name": "Nombre inexistente de categoria"
    })
}

mock_success ={
    "body": json.dumps({
        "id": 1,
        "name": "Test update category success"
    })
}

mock_missing_fields ={
    "body": json.dumps({
        "id": None,
        "name": "Nombre"
    })
}

mock_empty_fields ={
    "body": json.dumps({
        "id": 1,
        "name": ""
    })
}

class TestUpdateCategory(unittest.TestCase):

    @patch("update_category.app.category_exist")
    @patch("update_category.app.duplicated_name")
    def test_lambda_category_not_exists(self, mock_category_exist, mock_duplicated_name):
        mock_category_exist.return_value = False
        mock_duplicated_name.return_value = False

        result = app.lambda_handler(mock_category_not_exists, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 404)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORY_NOT_FOUND")

    @patch("update_category.app.category_exist")
    @patch("update_category.app.duplicated_name")
    def test_lambda_duplicated_name(self, mock_category_exist, mock_duplicated_name):
        mock_category_exist.return_value = True
        mock_duplicated_name.return_value = True

        result = app.lambda_handler(mock_name_duplicated, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DUPLICATED_NAME")

    @patch("update_category.app.duplicated_name")
    @patch("update_category.app.category_exist")
    def test_lambda_success(self, mock_category_exist, mock_duplicated_name):
        mock_duplicated_name.return_value = False
        mock_category_exist.return_value = True

        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORY_UPDATED")

    @patch("update_category.app.duplicated_name")
    @patch("update_category.app.category_exist")
    def test_lambda_missing_fields(self, mock_category_exist, mock_duplicated_name):
        mock_duplicated_name.return_value = False
        mock_category_exist.return_value = True

        result = app.lambda_handler(mock_empty_fields, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "EMPTY_FIELDS")

