import json
import pymysql
import logging

# Configuración de RDS (reemplaza con tus datos reales)
rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "cafe_balu"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, __):
    try:
        # 1. Obtener lista de productos y cantidades desde el cuerpo de la solicitud
        body = json.loads(event['body'])
        product_quantities = body.get('products', [])

        # 2. Validación de datos
        if not product_quantities:
            raise ValueError("La lista de productos está vacía")

        # 3. Obtener información de productos y calcular el total
        total = 0
        product_details = []
        for item in product_quantities:
            product_id = item['product_id']
            quantity = item['quantity']
            unit_price = obtener_precio_producto(product_id)
            if unit_price is None:
                raise ValueError(f"Producto no encontrado: {product_id}")
            total += quantity * unit_price
            product_details.append((product_id, quantity, unit_price))

        # 4. Registrar la venta en la tabla 'sales'
        sale_id = guardar_venta(body.get('status', 'pendiente'), total)
        logger.info("Venta registrada exitosamente con id=%s", sale_id)

        # 5. Registrar detalles en 'sales_products' (usando un solo INSERT)
        guardar_ventas_productos(sale_id, product_details)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "VENTA_Y_PRODUCTOS_GUARDADOS",
                "sale_id": sale_id
            })
        }

    except (KeyError, ValueError) as e:
        return {
            "statusCode": 400,  # Bad Request
            "body": json.dumps({
                "message": "Solicitud incorrecta",
                "error": str(e)
            })
        }
    except pymysql.Error as e:
        return {
            "statusCode": 500,  # Internal Server Error
            "body": json.dumps({
                "message": "Error en la base de datos",
                "error": str(e)
            })
        }
    except Exception as e:
        logger.error("Error inesperado: %s", str(e))
        raise  # Re-lanza la excepción para que Lambda la maneje

def obtener_precio_producto(product_id):
    with pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            return result[0] if result else None

def guardar_venta(status, total):
    with pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db) as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO sales (status, total) VALUES (%s, %s)", (status, total))
            sale_id = cursor.lastrowid
            connection.commit()
            return sale_id

def guardar_ventas_productos(sale_id, product_details):
    with pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db) as connection:
        with connection.cursor() as cursor:
            values = [(sale_id, p_id, qty, u_price) for p_id, qty, u_price in product_details]
            query = "INSERT INTO sales_products (sale_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)" * len(values)
            query = query[:-1]  # Eliminar la última coma
            cursor.execute(query, [item for sublist in values for item in sublist])
            connection.commit()