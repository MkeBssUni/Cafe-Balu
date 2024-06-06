import json
import pymysql
from decimal import Decimal

rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, __):
    try:

        if 'pathParameters' not in event:
            raise Exception

        status = event['pathParameters'].get('status')
        id = event['pathParameters'].get('id')
        type = event['pathParameters'].get('type')

        if status is None or id is None or type is None:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "MISSING_FIELDS"
                }),
            }

        change_status(id, type, status)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "STATUS_CHANGED"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }),
        }

def change_status(id, type, status):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        cursor = connection.cursor()
        query = ""

        if(type == 'PRODUCT'):
            query = "update products set status = %s where id = %s"

        if(type == 'CATEGORY'):
            query = "update categories set status = %s where id = %s"

        cursor.execute(query, (status,id))
        connection.commit()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }),
        }
    finally:
        connection.close()