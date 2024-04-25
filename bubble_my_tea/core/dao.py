from django.db import connection, transaction

# === Users ===
def create_user(first_name, last_name, email, password, role='user'):
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password, role)
                VALUES (%s, %s, %s, %s, %s)
            """, [first_name, last_name, email, password, role])

def get_user(email):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        return cursor.fetchone()
     
def get_user_credentials(email):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT password, first_name, role 
            FROM users 
            WHERE email = %s
        """, [email])
        return cursor.fetchone()

def update_user(email, first_name=None, last_name=None, password=None):
    updates = []
    params = []
    if first_name:
        updates.append("first_name = %s")
        params.append(first_name)
    if last_name:
        updates.append("last_name = %s")
        params.append(last_name)
    if password:
        updates.append("password = %s")
        params.append(password)
    params.append(email)
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE email = %s", params)

def delete_user(email):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE email = %s", [email])

# === Products ===
def create_product(name, description, price, image):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO products (name, description, price, image)
            VALUES (%s, %s, %s, %s)
        """, [name, description, price, image])

def get_all_products():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

def update_product(product_id, name=None, description=None, price=None, image=None):
    updates = []
    params = []
    if name:
        updates.append("name = %s")
        params.append(name)
    if description:
        updates.append("description = %s")
        params.append(description)
    if price:
        updates.append("price = %s")
        params.append(price)
    if image:
        updates.append("image = %s")
        params.append(image)
    params.append(product_id)
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE products SET {', '.join(updates)} WHERE id = %s", params)

def delete_product(product_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM products WHERE id = %s", [product_id])

# === Toppings ===
def create_topping(name, additional_price):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO toppings (name, additional_price)
            VALUES (%s, %s)
        """, [name, additional_price])

def get_all_toppings():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM toppings")
        return cursor.fetchall()

def update_topping(topping_id, name=None, additional_price=None):
    updates = []
    params = []
    if name:
        updates.append("name = %s")
        params.append(name)
    if additional_price:
        updates.append("additional_price = %s")
        params.append(additional_price)
    params.append(topping_id)
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE toppings SET {', '.join(updates)} WHERE id = %s", params)

def delete_topping(topping_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM toppings WHERE id = %s", [topping_id])

def get_product_by_id(product_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", [product_id])
        return cursor.fetchone()