import json
import unittest
from unittest.mock import patch
import pymysql
from update_product import app

mock_event_admin = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    },
    "body": json.dumps({
        "id": 1,
        "name": "New Product",
        "stock": 10,
        "price": 100,
        "status": 1,
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
        "category_id": 1,
        "url": "https://example.com/image.jpg"
    })
}

mock_event_missing_fields = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    },
    "body": json.dumps({
        "name": "New Product",
        "stock": 10,
        "price": 100,
        "status": 1,
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
        "category_id": 1,
        "url": "https://example.com/image.jpg"
    })
}

mock_event_invalid_image = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    },
    "body": json.dumps({
        "id": 1,
        "name": "New Product",
        "stock": 10,
        "price": 100,
        "status": 1,
        "image": "invalid_image_data",
        "category_id": 1,
        "url": "https://example.com/image.jpg"
    })
}

mock_event_forbidden = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["user"]
            }
        }
    },
    "body": json.dumps({
        "id": 1,
        "name": "New Product",
        "stock": 10,
        "price": 100,
        "status": 1,
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
        "category_id": 1,
        "url": "https://example.com/image.jpg"
    })
}

mock_event_category_not_found = {
    "requestContext": {
        "authorizer": {
            "claims": {
                "cognito:groups": ["admin"]
            }
        }
    },
    "body": json.dumps({
        "id": 1,
        "name": "New Product",
        "stock": 10,
        "price": 100,
        "status": 1,
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
        "category_id": 999,
        "url": "https://example.com/image.jpg"
    })
}

class TestUpdateProduct(unittest.TestCase):
    # Prueba de actualización exitosa del producto
    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_update_product_success(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        mock_event_admin["body"] = json.dumps({
            "id": 1,
            "name": "New Product",
            "stock": 10,
            "price": 100,
            "status": 1,
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
            "category_id": 1,
            "description": "A new product",
            "url": "https://example.com/image.jpg"
        })
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200, f"Se esperaba el código de estado 200 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "PRODUCT_UPDATED")

    # Prueba de actualización del producto con campos faltantes
    def test_update_product_missing_fields(self):
        result = app.lambda_handler(mock_event_missing_fields, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "MISSING_FIELDS")

    # Prueba de actualización del producto con datos de imagen inválidos
    @patch("update_product.app.category_exists")
    def test_update_product_invalid_image(self, mock_category_exists):
        mock_category_exists.return_value = True
        result = app.lambda_handler(mock_event_invalid_image, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        expected_message = "INVALID_IMAGE"
        self.assertEqual(body["message"], expected_message,
                         f"Se esperaba el mensaje '{expected_message}' pero se obtuvo '{body['message']}'")

    # Prueba de actualización del producto con acceso prohibido
    def test_update_product_forbidden(self):
        result = app.lambda_handler(mock_event_forbidden, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 403, f"Se esperaba el código de estado 403 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "FORBIDDEN")

    # Prueba de actualización del producto cuando la categoría no se encuentra
    @patch("update_product.app.category_exists")
    def test_update_product_category_not_found(self, mock_category_exists):
        mock_category_exists.return_value = False
        result = app.lambda_handler(mock_event_category_not_found, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORY_NOT_FOUND")

    # Prueba de la función de validación de imagen
    def test_is_invalid_image(self):
        valid_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
        invalid_image = "invalid_image_data"
        self.assertFalse(app.is_invalid_image(valid_image))
        self.assertTrue(app.is_invalid_image(invalid_image))

    # Prueba de descripción demasiado larga
    def test_update_product_description_too_long(self):
        long_description = "A" * 256
        mock_event_long_description = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": ["admin"]
                    }
                }
            },
            "body": json.dumps({
                "id": 1,
                "name": "New Product",
                "stock": 10,
                "price": 100,
                "status": 1,
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
                "category_id": 1,
                "description": long_description,
                "url": "https://example.com/image.jpg"
            })
        }
        result = app.lambda_handler(mock_event_long_description, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 413, f"Se esperaba el código de estado 413 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DESCRIPTION_TOO_LONG")

    # Prueba para manejar errores en la base de datos
    @patch("update_product.app.pymysql.connect")
    def test_update_product_database_error(self, mock_pymysql):
        mock_pymysql.side_effect = pymysql.MySQLError("Database error")
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500, f"Se esperaba el código de estado 500 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DATABASE_ERROR")

    # Prueba para manejar formato JSON inválido
    def test_update_product_invalid_json(self):
        mock_event_invalid_json = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": ["admin"]
                    }
                }
            },
            "body": "{invalid_json}"
        }
        result = app.lambda_handler(mock_event_invalid_json, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_JSON_FORMAT")
