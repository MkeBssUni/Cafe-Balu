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

        id = event['pathParameters'].get('id')

        if id is None:
            logger.warning("Missing fields: id")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS"
                }),
            }

        cancel_sale(id)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "SUCCESSFUL_CANCELLATION",
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

def cancel_sale(id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    print(connection)
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE sales SET status = 0 WHERE id=%s", (id,))
        connection.commit()
    except Exception as e:
        logger.error("Database update error: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "DATABASE_ERROR"
            }),
        }
    finally:
        connection.close()
