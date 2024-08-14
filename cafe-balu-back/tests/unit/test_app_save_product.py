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
    @patch("save_product.app.product_exists_in_category")
    @patch("save_product.app.pymysql.connect")
    def test_save_product_success(self, mock_connect, mock_product_exists, mock_category_exists,mock_upload_image_to_s3):
        mock_product_exists.return_value = False
        mock_category_exists.return_value = True
        mock_upload_image_to_s3.return_value = "https://example.com/image.jpg"

        # Configurar el mock para la conexión a la base de datos
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value

        # Convertir la cadena JSON en un diccionario
        body_dict = json.loads(mock_event_admin['body'])

        # Llamar a la función lambda_handler
        result = app.lambda_handler(mock_event_admin, None)

        # Verificar el código de estado y el cuerpo de la respuesta
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200, f"Se esperaba el código de estado 200 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "PRODUCT_ADDED")

        # Verificar que se llamó a cursor.execute con los parámetros correctos
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO products (name, stock, price, category_id, status, image, description) VALUES (%s, %s, %s, %s, true, %s, %s)",
            (
                body_dict['name'],
                body_dict['stock'],
                body_dict['price'],
                body_dict['category_id'],
                mock_upload_image_to_s3.return_value,
                "Sin descripción"
            )
        )

        # Verificar que se llamó a connection.commit
        mock_connection.commit.assert_called_once()
    @patch("save_product.app.category_exists")
    @patch("save_product.app.product_exists_in_category")
    @patch("save_product.app.pymysql.connect")
    def test_save_product_invalid_image(self, mock_connect, mock_product_exists, mock_category_exists):
        # Configurar los mocks
        mock_category_exists.return_value = True
        mock_product_exists.return_value = False

        # Configurar el mock para la conexión a la base de datos (opcional, si es necesario)
        mock_connection = mock_connect.return_value
        # ... puedes configurar el comportamiento del mock_connection si es necesario

        # Llamar a la función lambda_handler
        result = app.lambda_handler(mock_event_invalid_image, None)

        # Verificar el código de estado y el cuerpo de la respuesta
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400,f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_IMAGE")

        # Opcional: Verificar que NO se llamaron funciones de la base de datos
        mock_connection.cursor.assert_not_called()
    def test_save_product_forbidden(self):
        result = app.lambda_handler(mock_event_forbidden, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 403, f"Se esperaba el código de estado 403 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "FORBIDDEN")
    @patch("save_product.app.category_exists")
    def test_save_product_category_not_found(self, mock_category_exists):
        mock_category_exists.return_value = False
        result = app.lambda_handler(mock_event_category_not_found, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400, f"Se esperaba el código de estado 400 pero se obtuvo {status_code}. Respuesta: {result}")
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "CATEGORY_NOT_FOUND")
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
        app.add_product('New Product', 10, 100, 1, 'https://example.com/image.jpg','Description')  # Eliminamos el argumento 'status'
        mock_cursor.execute.assert_called_once_with("INSERT INTO products (name, stock, price, category_id, status, image, description) VALUES (%s, %s, %s, %s, true, %s, %s)",('New Product', 10, 100, 1, 'https://example.com/image.jpg', 'Description'))
    def test_save_product_invalid_name(self):
        invalid_name_event = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": ["admin"]
                    }
                }
            },
            "body": json.dumps({
                "name": "New Product!",  # Invalid name with special character
                "stock": 10,
                "price": 100,
                "status": 1,
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
                "category_id": 1,
                "url": "https://example.com/image.jpg"
            })
        }
        result = app.lambda_handler(invalid_name_event, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_NAME")
    def test_save_product_invalid_stock(self):
        invalid_stock_event = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": ["admin"]
                    }
                }
            },
            "body": json.dumps({
                "name": "New Product",
                "stock": -5,  # Invalid stock (negative)
                "price": 100,
                "status": 1,
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
                "category_id": 1,
                "url": "https://example.com/image.jpg"
            })
        }
        result = app.lambda_handler(invalid_stock_event, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_STOCK")
    def test_save_product_invalid_price(self):
        invalid_price_event = {
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
                "price": 0,  # Invalid price (zero)
                "status": 1,
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
                "category_id": 1,
                "url": "https://example.com/image.jpg"
            })
        }
        result = app.lambda_handler(invalid_price_event, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_PRICE")
    def test_save_product_invalid_category_id(self):
        invalid_category_id_event = {
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
                "category_id": -1,  # Invalid category_id (negative)
                "url": "https://example.com/image.jpg"
            })
        }
        result = app.lambda_handler(invalid_category_id_event, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INVALID_CATEGORY_ID")
    @patch("save_product.app.category_exists")
    @patch("save_product.app.product_exists_in_category")
    def test_save_product_already_exists(self, mock_product_exists, mock_category_exists):
        mock_category_exists.return_value = True
        mock_product_exists.return_value = True  # Simulate product already exists
        result = app.lambda_handler(mock_event_admin, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "PRODUCT_EXISTS")
    def test_save_product_missing_body_key(self):
        mock_event_missing_body = {
            "requestContext": {
                "authorizer": {
                    "claims": {
                        "cognito:groups": ["admin"]
                    }
                }
            }
            # No hay clave 'body'
        }
        result = app.lambda_handler(mock_event_missing_body, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "MISSING_KEY")
    def test_save_product_description_too_long(self):
        long_description_event = {
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
                "description": "a" * 256,  # Descripción de 256 caracteres (demasiado larga)
                "url": "https://example.com/image.jpg"
            })
        }
        result = app.lambda_handler(long_description_event, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 413)  # Esperamos un 413 para entidad demasiado grande
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "DESCRIPTION_TOO_LONG")
    @patch('pymysql.connect')
    def test_product_exists_in_category_exists(self, mock_connect):
        # Configurar el mock para simular que el producto existe
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (1,)  # Simula que hay 1 producto coincidente

        # Llamar a la función
        result = app.product_exists_in_category(1, 'Producto existente')

        # Verificar que la función devuelve True
        self.assertTrue(result)

        # Verificar que se ejecutó la consulta correcta
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) FROM products WHERE category_id = %s AND lower(name) = %s",
            (1, 'producto existente')
        )
    @patch('pymysql.connect')
    def test_product_exists_in_category_does_not_exist(self, mock_connect):
        # Configurar el mock para simular que el producto NO existe
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (0,)  # Simula que NO hay productos coincidentes

        # Llamar a la función
        result = app.product_exists_in_category(2, 'Producto no existente')

        # Verificar que la función devuelve False
        self.assertFalse(result)

        # Verificar que se ejecutó la consulta correcta
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) FROM products WHERE category_id = %s AND lower(name) = %s",
            (2, 'producto no existente')
        )
    @patch('pymysql.connect')
    def test_product_exists_in_category_database_error(self, mock_connect):
        # Configurar el mock para simular un error de base de datos
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = pymysql.MySQLError('Error simulado de base de datos')

        # Llamar a la función y verificar que lanza una excepción
        with self.assertRaises(pymysql.MySQLError):
            app.product_exists_in_category(3, 'Cualquier producto')
    def test_save_product_missing_fields(self):
        # Modificamos mock_event_missing_fields para que le falte un campo obligatorio, por ejemplo "name"
        mock_event_missing_fields['body'] = json.dumps({
            "stock": 10,
            "price": 100,
            "status": 1,
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
            "category_id": 1,
            "url": "https://example.com/image.jpg"
        })

        result = app.lambda_handler(mock_event_missing_fields, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "MISSING_FIELDS")
    @patch("save_product.app.pymysql.connect")  # Puedes necesitar otros mocks dependiendo de tu código
    def test_save_product_generic_exception(self, mock_connect):
        # Forzamos una excepción genérica, puedes ajustar esto según tu código
        mock_connect.side_effect = Exception("Alguna excepción inesperada")

        # Llamamos a la función lambda_handler
        result = app.lambda_handler(mock_event_admin, None)  # Usamos un evento válido

        # Verificamos el código de estado y el cuerpo de la respuesta
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)
        body = json.loads(result["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "INTERNAL_SERVER_ERROR")
        self.assertIn("error", body)
        self.assertEqual(body["error"], "Alguna excepción inesperada")
    @patch('pymysql.connect')
    def test_is_name_duplicate_true(self, mock_connect):
        # Configurar el mock para simular que el nombre está duplicado
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (1,)  # Simula que hay 1 producto con ese nombre

        # Llamar a la función
        result = app.is_name_duplicate('Producto existente')

        # Verificar que la función devuelve True
        self.assertTrue(result)

        # Verificar que se ejecutó la consulta correcta
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) FROM products WHERE lower(name) = %s",
            ('producto existente',)
        )
    @patch('pymysql.connect')
    def test_is_name_duplicate_false(self, mock_connect):
        # Configurar el mock para simular que el nombre NO está duplicado
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (0,)  # Simula que NO hay productos con ese nombre

        # Llamar a la función
        result = app.is_name_duplicate('Producto no existente')

        # Verificar que la función devuelve False
        self.assertFalse(result)

        # Verificar que se ejecutó la consulta correcta
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) FROM products WHERE lower(name) = %s",
            ('producto no existente',)
        )
    @patch('pymysql.connect')
    def test_is_name_duplicate_database_error(self, mock_connect):
        # Configurar el mock para simular un error de base de datos
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = pymysql.MySQLError('Error simulado de base de datos')

        # Llamar a la función y verificar que lanza una excepción
        with self.assertRaises(pymysql.MySQLError):
            app.is_name_duplicate('Cualquier producto')
    @patch('pymysql.connect')
    def test_category_exists_true(self, mock_connect):
        # Configurar el mock para simular que la categoría existe
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (1,)  # Simula que hay 1 categoría con ese ID

        # Llamar a la función
        result = app.category_exists(1)  # Supongamos que el ID de categoría es 1

        # Verificar que la función devuelve True
        self.assertTrue(result)

        # Verificar que se ejecutó la consulta correcta
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) FROM categories WHERE id = %s",
            (1,)
        )
    @patch('pymysql.connect')
    def test_category_exists_false(self, mock_connect):
        # Configurar el mock para simular que la categoría NO existe
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = (0,)  # Simula que NO hay categorías con ese ID

        # Llamar a la función
        result = app.category_exists(999)  # Supongamos que el ID de categoría es 999

        # Verificar que la función devuelve False
        self.assertFalse(result)

        # Verificar que se ejecutó la consulta correcta
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) FROM categories WHERE id = %s",
            (999,)
        )
    @patch('pymysql.connect')
    def test_category_exists_database_error(self, mock_connect):
        # Configurar el mock para simular un error de base de datos
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = pymysql.MySQLError('Error simulado de base de datos')

        # Llamar a la función y verificar que lanza una excepción
        with self.assertRaises(pymysql.MySQLError):
            app.category_exists(1)  # Puedes usar cualquier ID de categoría aquí


if __name__ == "__main__":
    unittest.main()