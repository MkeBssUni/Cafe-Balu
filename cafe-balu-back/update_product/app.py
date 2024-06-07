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
        if 'pathParameters' not in event:
            logger.error("pathParameters not found in the event")
            raise KeyError('pathParameters')

        params = event['pathParameters']
        required_params = ['id', 'name', 'stock', 'price', 'status', 'image', 'category_id']

        missing_params = [param for param in required_params if param not in params]
        if missing_params:
            logger.warning("Missing fields: %s", missing_params)
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS",
                    "missing": missing_params
                }),
            }

        product_id = params['id']
        name = params['name']
        stock = params['stock']
        price = params['price']
        status = params['status']
        image = params['image']
        category_id = params['category_id']

        update_product(product_id, name, stock, price, status, image, category_id)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "PRODUCT_UPDATED",
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


def update_product(product_id, name, stock, price, status, image, category_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    print(connection)
    try:
        cursor = connection.cursor()
        cursor.execute("""
                UPDATE products 
                SET name=%s, stock=%s, price=%s, status=%s, image=%s, category_id=%s 
                WHERE id=%s
            """, (name, stock, price, status, image, category_id, product_id))
        connection.commit()
        logger.info("Product updated successfully with id=%s", product_id)
    except Exception as e:
        logger.error("Database update error: %s", str(e))
        raise
    finally:
        connection.close()
