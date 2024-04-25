from django.urls import path

from .views import admin_dashboard, home, register, login, logout, product_detail, edit_product, profil

urlpatterns = [
    path('', home, name = 'home'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/product/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profil/', profil, name='profil'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]