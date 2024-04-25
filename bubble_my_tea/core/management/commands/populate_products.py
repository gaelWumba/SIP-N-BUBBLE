import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the products table with initial data using raw SQL'

    def handle(self, *args, **options):
        product_data = [
            {"name": "THÉ VERT À LA LIME", "description": "Un goût sucré et authentique avec un zeste de lime.", "price": 6.99, "image": "lime_tea.png"},
            {"name": "THÉ OOLONG À LA PÊCHE BLANCHE", "description": "Thé chinois Oolong fruité, parfumé et équilibré.", "price": 6.50, "image": "oolong_tea.png"},
            {"name": "THÉ VERT AU PAMPLEMOUSSE", "description": "Rafraîchissant et fruité avec une touche d’amertume.", "price": 6.50, "image": "pamplemousse_tea.png"},
            {"name": "THÉ VERT AU MIEL", "description": "Le goût herbacé et frais du thé vert, avec la douceur du miel.", "price": 5.40, "image": "honey_tea.png"},
            {"name": "SMOOTHIE AUX BISCUITS OREO", "description": "Crémeux, sucré et chocolaté, garni de biscuits. * Contient du lactose et du gluten", "price": 5.50, "image": "biscuits_tea.png"},
            {"name": "SMOOTHIE MATCHA HARICOT ROUGE", "description": "Un goût herbacé, légèrement sucré, crémeux, avec une texture légèrement farineuse.", "price": 6.99, "image": "rouge_tea.png"},
            {"name": "SMOOTHIE TARO", "description": "Légèrement sucré, crémeux, avec un délicieux goût de noisette.", "price": 6.99, "image": "taro_tea.png"},
            {"name": "CITRON MIEL ET MENTHE", "description": "Une limonade avec des touches florales, d’agrumes et de menthe.", "price": 5.50, "image": "menthe_tea.png"},
            {"name": "MELON D'HIVER ET CRÈME SEL DE MER", "description": "Sucré-salé avec une touche d’onctuosité.", "price": 5.50, "image": "creme_tea.png"},
            {"name": "PINA COLADA", "description": "Ananas, noix de coco crémeuse, barbotine sucrée et acidulée. * Disponible avec ou sans lait.", "price": 6.99, "image": "pina_tea.png"},
        ]

        sql = """
            INSERT INTO products (name, description, price, image) 
            VALUES (%s, %s, %s, %s)
        """

        with connection.cursor() as cursor:
            for product in product_data:
                cursor.execute(sql, [product['name'], product['description'], product['price'], product['image']])
            
            self.stdout.write(self.style.SUCCESS('Successfully populated products table using raw SQL.'))
