from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Sets up database tables'

    def handle(self, *args, **options):
        self.stdout.write("Creating tables...")
        with connection.cursor() as cursor:
            # User table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    email VARCHAR(255) UNIQUE,
                    password VARCHAR(255),
                    role ENUM('user', 'admin') DEFAULT 'user'
                );
            """)
            # Product table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    description TEXT,
                    price DECIMAL(10, 2),
                    image VARCHAR(255)  # Assuming simple image reference, adjust if using ImageField
                );
            """)
            # Topping table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS toppings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    additional_price DECIMAL(10, 2)
                );
            """)
            # ProductTopping join table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_toppings (
                    product_id INT,
                    topping_id INT,
                    is_default BOOLEAN DEFAULT FALSE,
                    PRIMARY KEY (product_id, topping_id),
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (topping_id) REFERENCES toppings(id)
                );
            """)
            # Order table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    order_date DATETIME,
                    status VARCHAR(50),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)
            # OrderDetail table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_details (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    product_id INT,
                    quantity INT,
                    sugar_level INT DEFAULT 100,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                );
            """)
            # OrderDetailTopping join table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_detail_toppings (
                    order_detail_id INT,
                    topping_id INT,
                    quantity INT DEFAULT 1,
                    PRIMARY KEY (order_detail_id, topping_id),
                    FOREIGN KEY (order_detail_id) REFERENCES order_details(id),
                    FOREIGN KEY (topping_id) REFERENCES toppings(id)
                );
            """)
        self.stdout.write(self.style.SUCCESS('Successfully created tables.'))
