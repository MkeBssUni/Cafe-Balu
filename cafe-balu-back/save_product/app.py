import json
import pymysql
import logging

rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, __):
    try:
        if 'body' not in event:
            logger.error("Request body not found in the event")
            raise KeyError('body')

        body = json.loads(event['body'])
        name = body.get('name')
        stock = body.get('stock')
        price = body.get('price')
        category_id = body.get('category_id')
        image = body.get('image')

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
        cursor.execute("INSERT INTO products (name, stock, price, category_id, status, image) VALUES (%s, %s, %s, %s, true, %s)", (name, stock, price, category_id, image))
        connection.commit()
        logger.info("Product added successfully: name=%s", name)
    except Exception as e:
        logger.error("Database insert error: %s", str(e))
        raise e
    finally:
        connection.close()