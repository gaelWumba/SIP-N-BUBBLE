"""Module containing models for the app."""
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, default='user')

    class Meta:
        managed = False 

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255)  

    class Meta:
        managed = False

class Topping(models.Model):
    name = models.CharField(max_length=255)
    additional_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = False

class ProductTopping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    class Meta:
        managed = False
        unique_together = (('product', 'topping'),)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=50)

    class Meta:
        managed = False

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sugar_level = models.IntegerField(default=100)  

    class Meta:
        managed = False

class OrderDetailTopping(models.Model):
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        managed = False