import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the products table with initial data using raw SQL'

    def handle(self, *args, **options):
        topping_data = [
            {"name": "TPERLES DE TAPIOCA", "additional_price": 2.50},
            {"name": "PERLES DE CASSONADE", "additional_price": 2.50},
            {"name": "PERLES DE SAKURA", "additional_price": 2.50},
            {"name": "HARICOT ROUGE", "additional_price": 2.40},
            {"name": "GELÉE ARC-EN-CIEL", "additional_price": 2.50},
            {"name": "GELÉE DE CAFÉ", "additional_price": 2.50},
            {"name": "GELÉE DE POUDING", "additional_price": 2.50},
            {"name": "GELÉE MATCHA", "additional_price": 2.50},
            {"name": "GELÉE D'HERBES", "additional_price": 2.50},
        ]

        sql = """
            INSERT INTO toppings (name, additional_price) 
            VALUES (%s, %s)
        """

        with connection.cursor() as cursor:
            for topping in topping_data:
                cursor.execute(sql, [topping['name'], topping['additional_price']])
            
            self.stdout.write(self.style.SUCCESS('Successfully populated toppings table using raw SQL.'))
