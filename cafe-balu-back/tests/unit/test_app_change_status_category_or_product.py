import unittest
import json

from botocore.exceptions import ClientError

from change_status_category_or_product import app
from unittest.mock import patch, Mock

# Mocking events
mock_change_status_category_success = {
    "body": json.dumps({
        "id": 1,
        "status": 1,
        "type": "CATEGORY"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

mock_change_status_product_success = {
    "body": json.dumps({
        "id": 1,
        "status": 1,
        "type": "PRODUCT"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

mock_change_status_missing_fields = {
    "body": json.dumps({
        "id": None,
        "status": None,
        "type": "PRODUCT"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

mock_change_status_invalid_status = {
    "body": json.dumps({
        "id": 1,
        "status": 123,
        "type": "PRODUCT"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

mock_change_status_invalid_type = {
    "body": json.dumps({
        "id": 1,
        "status": 1,
        "type": "INVALID_TYPE"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

mock_change_status_type_not_found = {
    "body": json.dumps({
        "id": 502,
        "status": 1,
        "type": "PRODUCT"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

mock_change_status_internal_server_error = {
    "body": json.dumps({
        "id": 1,
        "status": 1,
        "type": "PRODUCT"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

class TestChangeStatusCategoryOrProduct(unittest.TestCase):

    def test_lambda_change_status_category_success(self):
        result = app.lambda_handler(mock_change_status_category_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "STATUS_CHANGED")

    def test_lambda_change_status_product_success(self):
        result = app.lambda_handler(mock_change_status_product_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "STATUS_CHANGED")

    def test_lambda_change_status_missing_fields(self):
        result = app.lambda_handler(mock_change_status_missing_fields, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)  # Esperando un 400 por campos faltantes
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "MISSING_FIELDS")

    def test_lambda_change_status_invalid_status(self):
        result = app.lambda_handler(mock_change_status_invalid_status, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)  # Esperando un 400 por status inválido
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_STATUS")

    def test_lambda_change_status_invalid_type(self):
        result = app.lambda_handler(mock_change_status_invalid_type, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)  # Esperando un 400 por tipo inválido
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_TYPE_"+json.loads(mock_change_status_invalid_type["body"])["type"])

    @patch("change_status_category_or_product.app.type_exists")
    def test_lambda_change_status_type_not_found(self, mock_type_exists):
        mock_type_exists.return_value = False

        result = app.lambda_handler(mock_change_status_type_not_found, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 404)  # Esperando un 404 cuando el tipo no se encuentra
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], json.loads(mock_change_status_type_not_found["body"])["type"]+"_NOT_FOUND")

    def test_decimal_to_float_invalid_type(self):
        with self.assertRaises(TypeError):
            app.decimal_to_float("string")

    @patch("change_status_category_or_product.app.change_status")
    def test_lambda_change_status_internal_server_error(self, mock_change_status):
        mock_change_status.side_effect = Exception("Internal Server Error 5")
        result = app.lambda_handler(mock_change_status_internal_server_error, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)  # Esperando un 500 por error interno del servidor
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR_")

    @patch("change_status_category_or_product.app.boto3.session.Session.client")
    def test_get_secret_client_error(self, mock_client):
        # Simula la excepción ClientError
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_secret_value.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            operation_name='GetSecretValue'
        )

        with self.assertRaises(ClientError):
            app.get_secret()

    def test_lambda_handler_invalid_role(self):

        event = {
            "pathParameters": {
                "id": "1"
            },
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "invalidRole"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 403)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "FORBIDDEN")

    @patch("pymysql.connect")
    def test_change_status_exception(self, mock_connect):
        # Simula una excepción al ejecutar la consulta
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("Database execution error")
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Llamada directa a la función `change_status` para forzar el error
        with self.assertRaises(Exception) as context:
            app.change_status(1, 'PRODUCT', 1)

        self.assertEqual(str(context.exception), "Database execution error")