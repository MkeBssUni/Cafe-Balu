import json
import pymysql
import logging
import re

rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, __):
    try:
        body = json.loads(event.get('body', '{}'))
        name = body.get('name')

        if not name:
            logger.warning("Missing fields: name")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS"
                }),
            }

        # Verificar caracteres no permitidos
        if re.search(r'[<>/``\\{}]', name):
            logger.warning("Invalid characters in name")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "INVALID_CHARACTERS"
                }),
            }

        # Verificar nombre duplicado
        if is_name_duplicate(name):
            logger.warning("Duplicate category name: %s", name)
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "DUPLICATE_NAME"
                }),
            }

        save_category(name)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "CATEGORY_SAVED",
            }),
        }
    except json.JSONDecodeError:
        logger.error("Invalid JSON format")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "INVALID_JSON_FORMAT"
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

def is_name_duplicate(name):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories WHERE name = %s", (name,))
        result = cursor.fetchone()
        return result[0] > 0
    except Exception as e:
        logger.error("Database query error: %s", str(e))
        return False
    finally:
        connection.close()

def save_category(name):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO categories (name, status) VALUES (%s, true)", (name,))
        connection.commit()
        logger.info("Database create successfully for name=%s", name)
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
