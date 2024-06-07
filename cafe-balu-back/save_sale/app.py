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
        required_params = ['id', 'status', 'total']

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

        sale_id = params['id']
        status = params['status']
        total = params['total']

        save_sale(sale_id, status, total)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "SALE_SAVED",
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

def save_sale(sale_id, status, total):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    print(connection)
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sales (id, status, total) VALUES (%s, %s, %s)", (sale_id, status, total))
        connection.commit()
        logger.info("Sale recorded successfully with id=%s", sale_id)
    except Exception as e:
        logger.error("Database update error: %s", str(e))
        raise
    finally:
        connection.close()
