import unittest
import json
from unittest.mock import patch, MagicMock, Mock

from botocore.exceptions import ClientError

from save_category import app

class TestSaveCategory(unittest.TestCase):

    @patch("save_category.app.pymysql.connect")
    def test_lambda_handler_duplicate_name(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.execute.return_value = None
        mock_connect.return_value.cursor.return_value = mock_cursor

        event = {
            "body": json.dumps({
                "name": "duplicate"
            }),
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "DUPLICATE_NAME")

    @patch("save_category.app.pymysql.connect")
    def test_lambda_handler_valid(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (0,)
        mock_cursor.execute.return_value = None
        mock_connect.return_value.cursor.return_value = mock_cursor

        event = {
            "body": json.dumps({
                "name": "validname"
            }),
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "CATEGORY_SAVED")

    def test_lambda_handler_invalid_json(self):
        event = {
            "body": "invalid json",
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "INVALID_JSON_FORMAT")

    def test_lambda_handler_missing_name(self):
        event = {
            "body": "{}",
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "MISSING_FIELDS")

    def test_lambda_handler_invalid_characters(self):
        event = {
            "body": json.dumps({
                "name": "invalid<>name"
            }),
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "INVALID_CHARACTERS")

    @patch("save_category.app.pymysql.connect")
    def test_is_name_duplicate_true(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = app.is_name_duplicate("duplicate")
        self.assertTrue(result)

    @patch("save_category.app.pymysql.connect")
    def test_is_name_duplicate_false(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (0,)
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = app.is_name_duplicate("newcategory")
        self.assertFalse(result)
    def test_lambda_handler_invalid_role(self):
        event = {
            "body": json.dumps({
                "name": "validname"
            }),
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

    @patch("save_category.app.boto3.session.Session.client")
    def test_get_secret_client_error(self, mock_client):
        # Simula la excepción ClientError
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_secret_value.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            operation_name='GetSecretValue'
        )

        with self.assertRaises(ClientError):
            app.get_secret()

    def test_lambda_handler_missing_key(self):
        event = {
            "body": json.dumps({
                "name": "validname"
            }),
            "requestContext": {
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "MISSING_KEY")
        self.assertIn("error", body)

    @patch("save_category.app.is_name_duplicate")
    def test_lambda_handler_internal_server_error(self, mock_is_name_duplicate):
        mock_is_name_duplicate.side_effect = Exception("Unexpected error")

        event = {
            "body": json.dumps({
                "name": "validname"
            }),
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 500)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR")
        self.assertIn("error", body)
        self.assertEqual(body["error"], "Unexpected error")

    @patch("save_category.app.pymysql.connect")
    def test_save_category_database_error(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Database insert error")
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
        }

        result = app.save_category("validname", headers)

        self.assertEqual(result["statusCode"], 500)
        self.assertEqual(result["body"], json.dumps({"message": "DATABASE_ERROR"}))

if __name__ == "__main__":
    unittest.main()
