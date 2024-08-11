import unittest
import json
from unittest.mock import patch, Mock

import pymysql
from botocore.exceptions import ClientError

from cancel_sales import app

class TestCancelSales(unittest.TestCase):

    @patch("cancel_sales.app.pymysql.connect")
    def test_lambda_handler_successful_cancellation(self, mock_connect):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        event = {
            "pathParameters": {
                "id": "1"
            },
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
        self.assertEqual(body["message"], "SUCCESSFUL_CANCELLATION")

    def test_lambda_handler_missing_id(self):
        event = {
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

    def test_lambda_handler_invalid_id_format(self):
        event = {
            "pathParameters": {
                "id": "INVALID_ID"
            },
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
        self.assertEqual(body["message"], "INVALID_ID")

    def test_lambda_handler_invalid_id(self):
        event = {
            "pathParameters": {
                "id": "-1"
            },
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
        self.assertEqual(body["message"], "INVALID_ID")

    def test_lambda_handler_invalid_characters(self):
        event = {
            "pathParameters": {
                "id": "1<>"
            },
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

    @patch("cancel_sales.app.pymysql.connect")
    def test_lambda_handler_id_not_found(self, mock_connect):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (0,)
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        event = {
            "pathParameters": {
                "id": "999"
            },
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 404)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "ID_NOT_FOUND")

    @patch("cancel_sales.app.pymysql.connect")
    def test_lambda_handler_database_error(self, mock_connect):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("Database connection error")
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        event = {
            "pathParameters": {
                "id": "1111111"
            },
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            }
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 404)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "ID_NOT_FOUND")

    @patch("cancel_sales.app.boto3.session.Session.client")
    def test_get_secret_client_error(self, mock_client):
        # Simula la excepción ClientError
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_secret_value.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            operation_name='GetSecretValue'
        )

        with self.assertRaises(ClientError):
            app.get_secret()

    @patch("cancel_sales.app.pymysql.connect")
    def test_lambda_handler_invalid_role(self, mock_connect):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

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

    @patch("cancel_sales.app.pymysql.connect")
    def test_lambda_handler_id_none(self, mock_connect):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        event = {
            "pathParameters": {
            },
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

    @patch("cancel_sales.app.pymysql.connect")
    def test_cancel_sale_database_error(self, mock_connect):
        mock_connection = Mock()
        mock_cursor = Mock()

        mock_cursor.execute.side_effect = Exception("Database connection error")
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        result = app.cancel_sale(1)

        self.assertEqual(result["statusCode"], 500)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "DATABASE_ERROR")

    @patch("cancel_sales.app.pymysql.connect")
    def test_lambda_handler_mysql_error(self, mock_connect):
        # Simula un error de MySQL al intentar conectar
        mock_connect.side_effect = pymysql.MySQLError("MySQL database error")

        event = {
            "pathParameters": {
                "id": "1"
            },
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
        self.assertEqual(body["message"], "DATABASE_ERROR")
        self.assertIn("MySQL database error", body["error"])
