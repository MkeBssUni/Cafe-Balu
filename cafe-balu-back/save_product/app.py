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

        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON format: %s", str(e))
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_JSON_FORMAT"
                }),
            }

        name = body.get('name')
        stock = body.get('stock')
        price = body.get('price')
        category_id = body.get('category_id')
        image = body.get('image')

        # Validar campos faltantes: 'name', 'stock', 'price'
        missing_fields = [field for field in ['name', 'stock', 'price', 'image'] if body.get(field) is None]

        if missing_fields:
            logger.warning(f"Missing fields: {', '.join(missing_fields)}")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS",
                    "missing_fields": missing_fields
                }),
            }

        # Validar 'name': debe ser una cadena no vacía y sin caracteres inválidos
        if not isinstance(name, str) or not name.strip() or not re.match(r'^[\w\s.-]+$', name):
            logger.warning("Invalid name: %s", name)
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
                    "message": "MISSING_CATEGORY_ID"
                }),
            }

        if not category_exists(category_id):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "CATEGORY_NOT_FOUND"
                }),
            }

        if product_exists_in_category(category_id, name):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "PRODUCT_EXISTS"
                }),
            }

        if is_invalid_image(image):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_IMAGE"
                }),
            }

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
    except pymysql.MySQLError as e:
        logger.error("MySQL error: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "DATABASE_ERROR",
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

def category_exists(category_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories WHERE id = %s", (category_id,))
        connection.commit()
        return cursor.fetchone()[0] > 0

    except Exception as e:
        logger.error("Database select error: %s", str(e))
        raise e
    finally:
        connection.close()

def product_exists_in_category(category_id, name):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM products WHERE category_id = %s AND lower(name) = %s", (category_id, name.lower()))
        connection.commit()
        return cursor.fetchone()[0] > 0

    except Exception as e:
        logger.error("Database select error: %s", str(e))
        raise e
    finally:
        connection.close()

def is_name_duplicate(name):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM products WHERE lower(name) = %s", (name.lower(),))
        connection.commit()
        return cursor.fetchone()[0] > 0

    except Exception as e:
        logger.error("Database select error: %s", str(e))
        raise e
    finally:
        connection.close()

def is_invalid_image(image):
    pattern = r"^data:image/(png|jpg|jpeg);base64,([a-zA-Z0-9+/=]+)$"
    return not re.match(pattern, image)
