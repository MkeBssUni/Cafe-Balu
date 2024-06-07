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

        name = event['pathParameters'].get('name')

        if name is None:
            logger.warning("Missing fields: name")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS"
                }),
            }

        save_category(name)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "CATEGORY_SAVE",
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

def save_category(name):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    print(connection)
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO categories (name, status) VALUES (%s, true)", (name,))
        connection.commit()
        logger.info("Database Create successfully for name=%s", name)
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
