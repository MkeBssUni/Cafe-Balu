import json
import pymysql
import logging

rds_host = "cafe-balu-database.cfk0gawqspc8.ca-central-1.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    try:
        if 'pathParameters' not in event:
            logger.error("pathParameters not found in the event")
            raise KeyError('pathParameters')

        newName = event['pathParameters'].get('name')
        id = event['pathParameters'].get('id')

        if newName is None or id is None:
            logger.warning("Missing fields: id or newName")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS"
                }),
            }

        update_category(id, newName)

        logger.info("Category updated successfully: id=%s, newName=%s", id, newName)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "CATEGORY_UPDATED",
            }),
        }
    except KeyError as e:
        logger.error("Missing key in event: %s", str(e))
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "MISSING_KEY",
                "error": str(e)
            }),
        }
    except Exception as e:
        logger.error("Internal server error: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }),
        }

def update_category(id, newName):
    global connection
    try:
        connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE category SET name = %s WHERE id = %s", (newName, id))
            connection.commit()
            logger.info("Database updated successfully for id=%s", id)
        except Exception as e:
            logger.error("Database update error: %s", str(e))
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "DATABASE_ERROR"
                }),
            }
    except Exception as e:
        logger.error("Database connection error: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "CONNECTION_ERROR"
            }),
        }
    finally:
        connection.close()
