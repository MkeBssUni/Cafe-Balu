import unittest
import json
from update_category import app
from unittest.mock import patch

mock_name_duplicated = {
    "body": json.dumps({
        "id": 1,
        "name": "Nombre duplicado"
    })
}

mock_category_not_exists = {
    "body": json.dumps({
        "id": 1506,
        "name": "Nombre inexistente de categoria"
    })
}

class TestUpdateCategory(unittest.TestCase):

    @patch("update_category.app.category_exist")
    @patch("update_category.app.duplicated_name")
    def test_lambda_category_not_exists(self, mock_category_exist, mock_duplicated_name):
        mock_category_exist.return_value = True
        mock_duplicated_name.return_value = True

        result = app.lambda_handler(mock_category_not_exists, None)
        print(result)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 404)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORY_NOT_FOUND")

    @patch("update_category.app.category_exist")
    @patch("update_category.app.duplicated_name")
    def test_lambda_duplicated_name(self, mock_category_exist, mock_duplicated_name):
        mock_category_exist.return_value = True
        mock_duplicated_name.return_value = False

        result = app.lambda_handler(mock_name_duplicated, None)
        print(result)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 404)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DUPLICATED_NAME")
