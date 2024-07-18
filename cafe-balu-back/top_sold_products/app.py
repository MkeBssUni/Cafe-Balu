import json
import pymysql
from decimal import Decimal

rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"
def lambda_handler(event, __):
    try:
       category = None
       if 'body' in event:
           if 'category' in json.loads(event['body']):
            category = json.loads(event['body']).get('category')

       if category != None:
            if not category_exists(category):
                return {
                    "statusCode": 404,
                    "body": json.dumps({
                        "message": "CATEGORY_NOT_FOUND"
                    }),
                }
       top_products = get_top_sold_products(category)
       return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "PRODUCTS_FETCHED",
                "product": top_products
            }, default=decimal_to_float)
       }
        
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }),
        }

def get_top_sold_products(category):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    if category == None:
        cursor.execute("""
        SELECT
            p.name AS product_name,
            c.name AS category_name,
            SUM(sp.quantity) AS total_quantity_sold
            FROM
                sales_products sp
            JOIN
                products p ON sp.product_id = p.id
            JOIN
                categories c ON p.category_id = c.id
            JOIN
                sales s ON sp.sale_id = s.id
            WHERE
                s.status = 1
            GROUP BY
                p.name, c.name
            ORDER BY
                total_quantity_sold DESC
            LIMIT 10;""", ())
    else:
        cursor.execute("""
        SELECT
            p.name AS product_name,
            c.name AS category_name,
            SUM(sp.quantity) AS total_quantity_sold
            FROM
                sales_products sp
            JOIN
                products p ON sp.product_id = p.id
            JOIN
                categories c ON p.category_id = c.id
            JOIN
                sales s ON sp.sale_id = s.id
            WHERE
                s.status = 1 AND c.id = %s
            GROUP BY
                p.name, c.name
            ORDER BY
                total_quantity_sold DESC
            LIMIT 10;""", (category,))
    
    result = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
    return result

def category_exists(category):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("select * from categories where id = %s", (category))
    result = cursor.fetchone()
    connection.close()
    return result != None

def connect_to_database():
    try:
        connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
        return connection
    except pymysql.MySQLError as e:
        raise Exception("ERROR CONNECTING TO DATABASE: " + str(e))

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError