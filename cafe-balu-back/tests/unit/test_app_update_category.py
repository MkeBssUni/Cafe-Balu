import unittest
import json

from botocore.exceptions import ClientError

from update_category import app
from unittest.mock import patch

mock_name_duplicated = {
    "body": json.dumps({
        "id": 1,
        "name": "Pasteles"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_category_not_exists = {
    "body": json.dumps({
        "id": 1506,
        "name": "Nombre inexistente de categoria"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_success = {
    "body": json.dumps({
        "id": 1,
        "name": "Test update category success"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_missing_fields = {
    "body": json.dumps({
        "id": None,
        "name": "Nombre"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_empty_fields = {
    "body": json.dumps({
        "id": 1,
        "name": ""
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_invalid_fields = {
    "body": json.dumps({
        "id": 1,
        "name": " "
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_invalid_json = {
    "body": "{id: 1, name: Test update category}",
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_missing_body = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_none_fields = {
    "body": json.dumps({
        "id": 1,
        "name": None
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    }
}

mock_invalid_role = {
    "body": json.dumps({
        "id": 1,
        "name": "Test update category success"
    }),
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["invalidRole"]
            }
        }
    }
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
    @patch("update_category.app.update_category")
    def test_lambda_success(self, mock_update_category, mock_category_exist, mock_duplicated_name):
        mock_duplicated_name.return_value = False
        mock_category_exist.return_value = True

        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "PUT, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
        }

        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORY_UPDATED")

    @patch("update_category.app.duplicated_name")
    @patch("update_category.app.category_exist")
    def test_lambda_empty_fields(self, mock_category_exist, mock_duplicated_name):
        mock_duplicated_name.return_value = False
        mock_category_exist.return_value = True

        result = app.lambda_handler(mock_empty_fields, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "EMPTY_FIELDS")

    @patch("update_category.app.duplicated_name")
    @patch("update_category.app.category_exist")
    def test_lambda_invalid_fields(self, mock_category_exist, mock_duplicated_name):
        mock_duplicated_name.return_value = False
        mock_category_exist.return_value = True

        result = app.lambda_handler(mock_invalid_fields, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_FIELDS")

    def test_lambda_missing_body(self):
        result = app.lambda_handler(mock_missing_body, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "MISSING_KEY")

    @patch("update_category.app.pymysql.connect")
    def test_lambda_internal_server_error(self, mock_connect):
        mock_connect.side_effect = Exception("Connection error")

        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR")

    @patch("update_category.app.pymysql.connect")
    def test_category_exist_true(self, mock_connect):
        mock_connect.return_value.cursor.return_value.fetchone.return_value = (1, 'Category Name')

        result = app.category_exist(1)
        self.assertTrue(result)

    @patch("update_category.app.pymysql.connect")
    def test_category_exist_false(self, mock_connect):
        mock_connect.return_value.cursor.return_value.fetchone.return_value = None

        result = app.category_exist(1)
        self.assertFalse(result)

    @patch("update_category.app.pymysql.connect")
    def test_category_exist_db_error(self, mock_connect):
        mock_connect.return_value.cursor.side_effect = Exception("Database error")

        result = app.category_exist(1)
        self.assertFalse(result)
    @patch("update_category.app.boto3.session.Session.client")
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
        result = app.lambda_handler(mock_invalid_role, None)
        self.assertEqual(result["statusCode"], 403)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "FORBIDDEN")

    def test_lambda_handler_name_is_none(self):
        mock = {
            "body": json.dumps({
                "id": 1,
                "name": None
            }),
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": ["admin"]
                    }
                }
            }
        }

        result = app.lambda_handler(mock, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "MISSING_FIELDS")

    @patch("update_category.app.pymysql.connect")
    def test_duplicated_name_db_error(self, mock_connect):
        # Simula un error en la ejecución de la consulta
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.side_effect = Exception("Database error")

        result = app.duplicated_name("Error Name")
        self.assertFalse(result)

        mock_connection.close.assert_called_once()

    @patch("update_category.app.pymysql.connect")
    def test_update_category_success(self, mock_connect):
        # Simula una actualización exitosa de la categoría
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value

        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "PUT, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
        }

        result = app.update_category(1, "New Name", headers)
        self.assertEqual(result, None)  # Espera que no haya errores y se complete correctamente

        mock_cursor.execute.assert_called_once_with(
            "UPDATE categories SET name = %s WHERE id = %s", ("New Name", 1)
        )
        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("update_category.app.pymysql.connect")
    def test_update_category_database_error(self, mock_connect):
        # Simula un error durante la ejecución del query
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.side_effect = Exception("Simulated database error")

        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "PUT, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
        }

        result = app.update_category(1, "New Name", headers)
        self.assertEqual(result["statusCode"], 500)
        self.assertEqual(result["body"], json.dumps({"message": "DATABASE_ERROR"}))

        mock_connection.close.assert_called_once()