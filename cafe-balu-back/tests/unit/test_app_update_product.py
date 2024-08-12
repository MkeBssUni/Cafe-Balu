import base64
import json
import unittest
from unittest.mock import patch
import pymysql
from botocore.exceptions import ClientError

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

    @patch("update_product.app.boto3.session.Session.client")
    def test_get_secret_client_error(self, mock_client):
        # Simula la excepción ClientError
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_secret_value.side_effect = ClientError(
            error_response={'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            operation_name='GetSecretValue'
        )

        with self.assertRaises(ClientError):
            app.get_secret()

    @patch("update_product.app.s3.put_object")
    def test_upload_image_to_s3(self, mock_put_object):
        # Datos de prueba
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

    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_update_product_description_none(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
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
            "description": "",
            "url": "https://example.com/image.jpg"
        })
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200, f"Se esperaba el código de estado 200 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "PRODUCT_UPDATED")

    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_update_product_invalid_name(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        mock_event_admin["body"] = json.dumps({
            "id": 1,
            "name": "",
            "stock": 10,
            "price": 100,
            "status": 1,
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
            "category_id": 1,
            "description": "",
            "url": "https://example.com/image.jpg"
        })
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_NAME")

    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_update_product_invalid_stock(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        mock_event_admin["body"] = json.dumps({
            "id": 1,
            "name": "Valid name",
            "stock": -2,
            "price": 100,
            "status": 1,
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
            "category_id": 1,
            "description": "",
            "url": "https://example.com/image.jpg"
        })
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_STOCK")

    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_update_product_invalid_price(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        mock_event_admin["body"] = json.dumps({
            "id": 1,
            "name": "Valid name",
            "stock": 5,
            "price": 0,
            "status": 1,
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
            "category_id": 1,
            "description": "",
            "url": "https://example.com/image.jpg"
        })
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_PRICE")

    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_update_product_invalid_category(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        mock_event_admin["body"] = json.dumps({
            "id": 1,
            "name": "Valid name",
            "stock": 2,
            "price": 100,
            "status": 1,
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
            "category_id": 0,
            "description": "",
            "url": "https://example.com/image.jpg"
        })
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_CATEGORY_ID")

    @patch('update_product.app.product_exists_in_category')
    def test_product_exists_in_category(self, mock_product_exists_in_category):
        # Simula que el producto ya existe en la categoría
        mock_product_exists_in_category.return_value = True

        # Datos de prueba
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'cognito:groups': 'admin'
                    }
                }
            },
            'body': json.dumps({
                'id': 1,
                'name': 'Product 1',
                'stock': 10,
                'price': 20.5,
                'status': 'available',
                'image': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD...',
                'category_id': 2,
                'url': 'http://example.com/image.jpg'
            })
        }

        response = app.lambda_handler(event, None)

        expected_response = {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
            },
            "body": json.dumps({
                "message": "PRODUCT_EXISTS"
            })
        }

        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['body'], json.dumps({"message": "PRODUCT_EXISTS"}))
        self.assertEqual(response['headers'], expected_response['headers'])

    def test_lambda_handler_missing_key(self):
        event = {
             'requestContext': {
                'authorizer': {
                    'claims': {
                        'cognito:groups': 'admin'
                    }
                }
            },
        }

        result = app.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 400)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "MISSING_KEY")
        self.assertIn("error", body)

    @patch("update_product.app.pymysql.connect")
    def test_update_product_success(self, mock_connect):
        # Simula una conexión y ejecución exitosa del query
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value

        # Llama a la función update_product
        app.update_product(1, 'Product 1', 10, 20.5, 'available', 'https://example.com/image.jpg', 2, 'Descripción del producto')

        # Verifica que se haya llamado a cursor.execute con el query correcto
        mock_cursor.execute.assert_called_once_with("""
            UPDATE products 
            SET name=%s, stock=%s, price=%s, status=%s, image=%s, category_id=%s, description=%s 
            WHERE id=%s
        """, ('Product 1', 10, 20.5, 'available', 'https://example.com/image.jpg', 2, 'Descripción del producto', 1))

        # Verifica que se haya hecho commit
        mock_connection.commit.assert_called_once()

        # Verifica que se haya cerrado la conexión
        mock_connection.close.assert_called_once()

    @patch("update_product.app.pymysql.connect")
    def test_update_product_database_error(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.side_effect = pymysql.MySQLError("Simulated database error")

        # Verifica que se levanta la excepción
        with self.assertRaises(pymysql.MySQLError):
            app.update_product(1, 'Product 1', 10, 20.5, 'available', 'https://example.com/image.jpg', 2, 'Descripción del producto')

        # Verifica que la conexión se cerró
        mock_connection.close.assert_called_once()

    @patch("update_product.app.pymysql.connect")
    def test_update_product_exception(self, mock_connect):
        mock_connect.side_effect = Exception("Simulated connection error")

        with self.assertRaises(Exception):
            app.update_product(1, 'Product 1', 10, 20.5, 'available', 'https://example.com/image.jpg', 2, 'Descripción del producto')

        mock_connect.return_value.close.assert_not_called()

    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_database_error_handling(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        mock_update_product.side_effect = pymysql.MySQLError("Simulated database error")

        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]

        self.assertEqual(status_code, 500, f"Se esperaba el código de estado 500 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DATABASE_ERROR")
        self.assertIn("error", body)
        self.assertEqual(body["error"], "Simulated database error")

    @patch("update_product.app.update_product")
    @patch("update_product.app.category_exists")
    @patch("update_product.app.upload_image_to_s3")
    def test_internal_server_error_handling(self, mock_upload_image_to_s3, mock_category_exists, mock_update_product):
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"
        mock_update_product.side_effect = Exception("Simulated internal error")

        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]

        self.assertEqual(status_code, 500, f"Se esperaba el código de estado 500 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR")
        self.assertIn("error", body)
        self.assertEqual(body["error"], "Simulated internal error")

    @patch("update_product.app.pymysql.connect")
    def test_category_exists_exception_handling(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.side_effect = Exception("Simulated query error")

        with self.assertRaises(Exception) as context:
            app.category_exists(1)

        self.assertEqual(str(context.exception), "Simulated query error")

        mock_connection.close.assert_called_once()