import json
import pymysql
import logging

# Configuración de RDS (reemplaza con tus datos reales)
rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, __):
    #arreglo de productos
    try:
        if 'body' not in event:
            logger.error("Request body not found in the event")
            raise KeyError('body')

        body=json.loads(event['body'])
        products = body.get('products')
        total = body.get('total')

        if not products or not total:
            logger.error("Products or total not found in the body")
            raise KeyError('products or total')

        products_info = get_products_info(products)

        response = save_sale(products_info, total)

        return response

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "BAD_REQUEST",
                "error": str(e)
            })
        }

def get_products_info(products):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        products_info = []

        for product in products:
            cursor.execute("select id, price, stock from products where id = %s", (product['id'],))
            product_info = cursor.fetchone()

            if product_info is None:
                raise ValueError(f"Product with id {product['id']} not found")

            if product_info[2] < product['quantity']:
                raise ValueError(f"Product with id {product['id']} has not enough stock")

            products_info.append({
                "id": product_info[0],
                "price": product_info[1],
                "quantity": product['quantity']
            })

        return products_info
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "DATABASE_ERROR",
                "error": str(e)
            }),
        }
    finally:
        connection.close()

def save_sale(products_info,total):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        cursor.execute("insert into sales (total, status) values (%s , 1)", (total,))
        sale_id = cursor.lastrowid

        for product in products_info:
            cursor.execute("insert into sales_products (sale_id, product_id, quantity) values (%s, %s, %s)", (sale_id, product['id'], product['quantity']))
            cursor.execute("update products set stock = stock - %s where id = %s", (product['quantity'], product['id']))

        connection.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "SALE_SAVED",
                "sale_id": sale_id
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "DATABASE_ERROR",
                "error": str(e)
            }),
        }
    finally:
        connection.close()