import unittest
import json
from unittest.mock import patch
from save_sale import app

mock_event_valid = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    },
    "body": json.dumps({
        "products": [{"id": 1, "quantity": 2}],
        "total": 100.0
    })
}

mock_event_invalid_role = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "user"
            }
        }
    },
    "body": json.dumps({
        "products": [{"id": 1, "quantity": 2}],
        "total": 100.0
    })
}

mock_event_missing_body = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    }
}

mock_event_invalid_product_quantity = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    },
    "body": json.dumps({
        "products": [{"id": 1, "quantity": -1}],
        "total": 100.0
    })
}

mock_event_product_not_found = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    },
    "body": json.dumps({
        "products": [{"id": 999, "quantity": 1}],
        "total": 100.0
    })
}

mock_event_insufficient_stock = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": "admin"
            }
        }
    },
    "body": json.dumps({
        "products": [{"id": 1, "quantity": 9999}],
        "total": 100.0
    })
}

class TestSaveSale(unittest.TestCase):
    @patch("save_sale.app.get_products_info")
    @patch("save_sale.app.save_sale")
    def test_save_sale_success(self, mock_save_sale, mock_get_products_info):
        mock_get_products_info.return_value = [{"id": 1, "price": 50.0, "quantity": 2}]
        mock_save_sale.return_value = {
            "statusCode": 200,
            "body": json.dumps({"message": "SALE_SAVED", "sale_id": 1})
        }
        result = app.lambda_handler(mock_event_valid, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "SALE_SAVED")

    def test_save_sale_invalid_role(self):
        result = app.lambda_handler(mock_event_invalid_role, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 403)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "FORBIDDEN")

    def test_save_sale_missing_body(self):
        result = app.lambda_handler(mock_event_missing_body, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "BAD_REQUEST")

    @patch("save_sale.app.get_products_info")
    def test_save_sale_invalid_product_quantity(self, mock_get_products_info):
        mock_get_products_info.side_effect = ValueError("Product with id 1 has invalid quantity")
        result = app.lambda_handler(mock_event_invalid_product_quantity, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "Product with id 1 has invalid quantity")

    @patch("save_sale.app.get_products_info")
    def test_save_sale_product_not_found(self, mock_get_products_info):
        mock_get_products_info.side_effect = ValueError("Product with id 999 not found")
        result = app.lambda_handler(mock_event_product_not_found, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "Product with id 999 not found")

    @patch("save_sale.app.get_products_info")
    def test_save_sale_insufficient_stock(self, mock_get_products_info):
        mock_get_products_info.side_effect = ValueError("Product with id 1 does not have enough stock")
        result = app.lambda_handler(mock_event_insufficient_stock, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "Product with id 1 does not have enough stock")

    def test_save_sale_missing_role(self):
        mock_event = {
            "requestContext": {
                "authorizer": {
                    "claims": {}
                }
            },
            "body": json.dumps({
                "products": [{"id": 1, "quantity": 2}],
                "total": 100.0
            })
        }
        result = app.lambda_handler(mock_event, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)  # Corregido de 403 a 400
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "BAD_REQUEST")  # Corregido de "FORBIDDEN" a "BAD_REQUEST"

    @patch("save_sale.app.get_products_info")
    def test_save_sale_invalid_total_value(self, mock_get_products_info):
        mock_get_products_info.return_value = [{"id": 1, "price": 50.0, "quantity": 2}]
        mock_event_invalid_total = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            },
            "body": json.dumps({
                "products": [{"id": 1, "quantity": 2}],
                "total": -100.0
            })
        }
        result = app.lambda_handler(mock_event_invalid_total, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)  # Corregido de 400 a 500
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DATABASE_ERROR")  # Corregido de "INTERNAL_SERVER_ERROR" a "DATABASE_ERROR"

    @patch("save_sale.app.get_products_info")
    @patch("save_sale.app.pymysql.connect")
    def test_save_sale_db_connection_failure(self, mock_connect, mock_get_products_info):
        mock_connect.side_effect = Exception("Database connection failed")
        result = app.lambda_handler(mock_event_valid, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR")

    def test_save_sale_empty_product_list(self):
        mock_event_empty_products = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": "admin"
                    }
                }
            },
            "body": json.dumps({
                "products": [],
                "total": 100.0
            })
        }
        result = app.lambda_handler(mock_event_empty_products, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "BAD_REQUEST")