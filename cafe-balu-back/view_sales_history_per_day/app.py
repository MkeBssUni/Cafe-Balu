import json
import pymysql
from datetime import datetime, timedelta
from decimal import Decimal
import logging

rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def validate_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        if date_obj > datetime.now():
            return False
        return True
    except ValueError:
        return False

def validate_date_range(start_date, end_date):
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        return start_date_obj < end_date_obj
    except ValueError:
        return False

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            logger.error("body not found in the event")
            raise KeyError('body')

        # Decodificar el cuerpo como JSON
        body = json.loads(event['body'])
        start_date = body.get('startDate')
        end_date = body.get('endDate')

        if not start_date or not end_date:
            logger.warning("Missing fields: startDate or endDate")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS"
                }),
            }

        if not validate_date(start_date) or not validate_date(end_date):
            logger.warning("Invalid date format or future date")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_DATE_FORMAT_OR_FUTURE_DATE"
                }),
            }

        if not validate_date_range(start_date, end_date):
            logger.warning("End date must be greater than start date")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "END_DATE_BEFORE_START_DATE"
                }),
            }

        sales = history_per_day(start_date, end_date)

        # Agrupar ventas por sales_id y seleccionar una vez el createdAt, status y total
        grouped_sales = {}
        for sale in sales:
            sale_id = sale['sale_id']
            if sale_id not in grouped_sales:
                grouped_sales[sale_id] = {
                    "sale_id": sale_id,
                    "createdAt": sale["createdAt"].strftime('%Y-%m-%d %H:%M:%S'),
                    "status": sale["status"],
                    "total": float(sale["total"]),
                    "products": []
                }
            grouped_sales[sale_id]["products"].append({
                "product_id": sale["product_id"],
                "name": sale["name"],
                "price": float(sale["price"])
            })

        return {
            "statusCode": 200,
            "body": json.dumps(list(grouped_sales.values()), default=decimal_to_float),
        }
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "MISSING_KEY",
                "error": str(e)
            }),
        }
    except Exception as e:
        logger.error(f"Exception: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }),
        }

def history_per_day(start_date, end_date):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT
                sales.id AS sale_id,
                sales.createdAt,
                sales.status,
                sales.total,
                products.id AS product_id,
                products.name,
                products.price
            FROM
                sales
            INNER JOIN
                sales_products
            ON
                sales.id = sales_products.sale_id
            INNER JOIN
                products
            ON
                sales_products.product_id = products.id
            WHERE
                sales.createdAt >= %s AND sales.createdAt < %s;
        """
        # Ajustar la fecha final para incluir hasta el final del día
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        cursor.execute(query, (start_date, end_date))
        sales = cursor.fetchall()
        return sales
    except Exception as e:
        logger.error(f"Database query error: {str(e)}", exc_info=True)
        raise
    finally:
        connection.close()