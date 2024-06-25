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

        newName = body.get('name')
        id = body.get('id')

        if newName is None or id is None:
            logger.warning("Missing fields: id or newName")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS"
                }),
            }

        if id == "" or newName == "":
            logger.warning("Empty fields: id or newName")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "EMPTY_FIELDS"
                }),
            }

        if not isinstance(newName, str) or len(newName.strip()) == 0:
            logger.warning("Invalid fields: newName")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_FIELDS"
                }),
            }

        id = int(id)
        newName = newName.strip()
        exist = category_exist(id)
        if category_exist(id) is False:
                logger.error("Category not found for id=%s", id)
                return {
                    "statusCode": 404,
                    "body": json.dumps({
                        "message": "CATEGORY_NOT_FOUND"
                    }),
                }

        if duplicated_name(newName) is True:
            logger.error("Category already exists: newName=%s", newName)
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "DUPLICATED_NAME"
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
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    print(connection)
    try:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE categories SET name = %s WHERE id = %s", (newName, id))
            connection.commit()
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

def category_exist(id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM categories WHERE id = %s", (id))
            result = cursor.fetchone()
            print("result", result)

            if result is None:
                return False

            return True
        except Exception as e:
            logger.error("Database error: %s", str(e))
            return False
    except Exception as e:
        logger.error("Database connection error: %s", str(e))
        return False
    finally:
        connection.close()

def duplicated_name(newName):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM categories WHERE lower(name) = %s", (newName.lower()))
            result = cursor.fetchone()
            print("result", result)

            if result is None:
                return False

            return True
        except Exception as e:
            logger.error("Database error: %s", str(e))
            return False
    except Exception as e:
        logger.error("Database connection error: %s", str(e))
        return False
    finally:
        connection.close()