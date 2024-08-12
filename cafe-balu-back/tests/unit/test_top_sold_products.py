import unittest
import json
from unittest.mock import patch

import pymysql
from botocore.exceptions import ClientError

from top_sold_products import app

mock_no_category = {
    "body": json.dumps({

    })
}

mock_category = {
    "body": json.dumps({
        "category" : 1
    })
}

mock_category_not_found = {
    "body": json.dumps({
        "category" : 999
    })
}

class TestTopSoldProducts(unittest.TestCase):
    def test_top_sold_products_no_category(self):
        result = app.lambda_handler(mock_no_category, None)
        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "PRODUCTS_FETCHED")

    def test_top_sold_products_with_category(self):
        result = app.lambda_handler(mock_category, None)
        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "PRODUCTS_FETCHED")
    def test_top_sold_products_category_not_found(self):
        result = app.lambda_handler(mock_category_not_found, None)
        self.assertEqual(result["statusCode"], 404)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "CATEGORY_NOT_FOUND")

    @patch("top_sold_products.app.connect_to_database")
    def test_top_sold_products_error_connecting(self, mock_connect_to_database):
        mock_connect_to_database.side_effect = Exception('Error')

        result = app.lambda_handler(mock_category, None)
        self.assertEqual(result["statusCode"], 500)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR")

    def test_decimal_to_float_invalid_type(self):
        with self.assertRaises(TypeError):
            app.decimal_to_float("string")

    @patch("top_sold_products.app.boto3.session.Session.client")
    def test_get_secret_client_error(self, mock_client):
        # Simula la excepción ClientError
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_secret_value.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            operation_name='GetSecretValue'
        )

        with self.assertRaises(ClientError):
            app.get_secret()

    @patch("top_sold_products.app.pymysql.connect")
    def test_connect_to_database_mysql_exception(self, mock_connect):
        # Simula una excepción MySQLError cuando se intenta conectar a la base de datos
        mock_connect.side_effect = pymysql.MySQLError("Simulated MySQL connection error")

        with self.assertRaises(Exception) as context:
            app.connect_to_database()

        # Verifica que la excepción levantada contiene el mensaje esperado
        self.assertIn("ERROR CONNECTING TO DATABASE", str(context.exception))
        self.assertIn("Simulated MySQL connection error", str(context.exception))