import json
import pymysql
import logging
import re

rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, __):
    try:
        # Validar presencia del campo 'body' en el evento
        if 'body' not in event:
            logger.error("Request body not found in the event")
            raise KeyError('body')

        body = json.loads(event['body'])
        name = body.get('name')
        stock = body.get('stock')
        price = body.get('price')
        category_id = body.get('category_id')
        image = body.get('image')

        # Validar campos faltantes: 'name', 'stock', 'price'
        missing_fields = [field for field in ['name', 'stock', 'price'] if body.get(field) is None]

        if missing_fields:
            logger.warning(f"Missing fields: {', '.join(missing_fields)}")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS",
                    "missing_fields": missing_fields
                }),
            }

        # Validar 'name': debe ser una cadena no vacía
        if not isinstance(name, str) or not name.strip():
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_NAME"
                }),
            }

        # Validar 'stock': debe ser un entero mayor o igual a cero
        if not isinstance(stock, int) or stock < 0:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_STOCK"
                }),
            }

        # Validar 'price': debe ser un número mayor a cero
        if not isinstance(price, (int, float)) or price <= 0:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_PRICE"
                }),
            }

        # Validar 'category_id' (opcional): si está presente, debe ser un entero positivo
        if category_id is not None and (not isinstance(category_id, int) or category_id <= 0):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_CATEGORY_ID"
                }),
            }

        # Validar 'image' URL (opcional): si está presente, debe ser una URL válida
        if image is not None:
            url_pattern = re.compile(r'^(https?://[^\s]+)$')
            if not isinstance(image, str) or not url_pattern.match(image):
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "INVALID_IMAGE_URL"
                    }),
                }

        # Llamar a la función para añadir el producto a la base de datos
        add_product(name, stock, price, category_id, image)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "PRODUCT_ADDED",
            }),
        }
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "MISSING_KEY",
                "error": str(e)
            }),
        }
    except Exception as e:
        logger.error("Exception: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }),
        }

def add_product(name, stock, price, category_id, image):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO products (name, stock, price, category_id, status, image) VALUES (%s, %s, %s, %s, true, %s)",
                       (name, stock, price, category_id, image))
        connection.commit()
        logger.info("Product added successfully: name=%s", name)
    except Exception as e:
        logger.error("Database insert error: %s", str(e))
        raise e
    finally:
        connection.close()