import base64
import json
import unittest
from unittest.mock import patch
import pymysql
from botocore.exceptions import ClientError

from save_product import app  # Asegúrate de importar tu función Lambda desde el módulo correcto

# Eventos de prueba
mock_event_admin = {
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
        "name": "New Product",
        "stock": 10,
        "price": 100,
        "status": 1,
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
        "category_id": 999,
        "url": "https://example.com/image.jpg"
    })
}

class TestSaveProduct(unittest.TestCase):
    # Prueba de guardado exitoso del producto
    @patch("save_product.app.upload_image_to_s3")
    @patch("save_product.app.category_exists")
    @patch("save_product.app.save_product")
    def test_save_product_success(self, mock_save_product, mock_category_exists, mock_upload_image_to_s3):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200, f"Se esperaba el código de estado 200 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "PRODUCT_SAVED")

    # Prueba de guardado del producto con campos faltantes
    def test_save_product_missing_fields(self):
        result = app.lambda_handler(mock_event_missing_fields, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "MISSING_FIELDS")

    # Prueba de guardado del producto con datos de imagen inválidos
    @patch("save_product.app.category_exists")
    def test_save_product_invalid_image(self, mock_category_exists):
        mock_category_exists.return_value = True
        result = app.lambda_handler(mock_event_invalid_image, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_IMAGE")

    # Prueba de guardado del producto con acceso prohibido
    def test_save_product_forbidden(self):
        result = app.lambda_handler(mock_event_forbidden, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 403, f"Se esperaba el código de estado 403 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "FORBIDDEN")

    # Prueba de guardado del producto cuando la categoría no se encuentra
    @patch("save_product.app.category_exists")
    def test_save_product_category_not_found(self, mock_category_exists):
        mock_category_exists.return_value = False
        result = app.lambda_handler(mock_event_category_not_found, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORY_NOT_FOUND")

    # Prueba para manejar errores en la base de datos
    @patch("save_product.app.pymysql.connect")
    def test_save_product_database_error(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.side_effect = pymysql.MySQLError("Database error")
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500, f"Se esperaba el código de estado 500 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DATABASE_ERROR")

    # Prueba para manejar formato JSON inválido
    def test_save_product_invalid_json(self):
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

    @patch("save_product.app.boto3.session.Session.client")
    def test_get_secret_client_error(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_secret_value.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            operation_name='GetSecretValue'
        )
        with self.assertRaises(ClientError):
            app.get_secret()

    @patch("save_product.app.s3.put_object")
    def test_upload_image_to_s3(self, mock_put_object):
        base64_image = "data:image/jpeg;base64," + base64.b64encode(b"test image data").decode('utf-8')
        url = "https://example.com/path/to/image.jpg"
        result_url = app.upload_image_to_s3(base64_image, url)
        expected_file_name = "images/image.jpg"
        expected_url = f"https://{app.bucket_name}.s3.amazonaws.com/{expected_file_name}"
        self.assertEqual(result_url, expected_url)
        mock_put_object.assert_called_once_with(
            Bucket=app.bucket_name,
            Key=expected_file_name,
            Body=base64.b64decode(base64_image.split(",")[1]),
            ContentType='image/jpeg'
        )

    @patch("save_product.app.pymysql.connect")
    def test_save_product_success_db(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        app.save_product('New Product', 10, 100, 1, 'https://example.com/image.jpg', 1, 'Description')
        mock_cursor.execute.assert_called_once_with("INSERT INTO products (name, stock, price, status, image_url, category_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s)",('New Product', 10, 100, 1, 'https://example.com/image.jpg', 1, 'Description'))

if __name__ == "__main__":
    unittest.main()
