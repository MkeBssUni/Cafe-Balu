import json
import pymysql
from datetime import datetime
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
    raise TypeError

def validate_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, '%Y/%m/%d')
        if date_obj > datetime.now():
            return False
        return True
    except ValueError:
        return False

def lambda_handler(event, __):
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

        sales = history_per_day(start_date, end_date)
        return {
            "statusCode": 200,
            "body": json.dumps(sales, default=decimal_to_float),
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
        query = "SELECT * FROM sales WHERE createdAt BETWEEN %s AND %s;"
        cursor.execute(query, (start_date, end_date))
        sales = cursor.fetchall()
        return sales
    except Exception as e:
        logger.error(f"Database query error: {str(e)}", exc_info=True)
        raise
    finally:
        connection.close()
