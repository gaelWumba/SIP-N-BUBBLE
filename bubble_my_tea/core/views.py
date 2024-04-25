import datetime
from django.db import connection
import jwt
import bcrypt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators.decorators import admin_required
from .forms import RegistrationForm, LoginForm, UpdateProductForm
from .dao import create_user, get_user_credentials, get_all_products, get_product_by_id, update_product, get_user

# === User Authentication Views ===
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_bytes = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
            create_user(first_name, last_name, email, hashed_password)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'hide_header': True})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            result = get_user_credentials(email)
            if result:
                user_password, first_name, role = result
                if bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                    token = jwt.encode({
                        'email': email,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                    }, settings.SECRET_KEY, algorithm='HS256')
                    response = redirect('admin_dashboard' if role == 'admin' else 'home')
                    response.set_cookie(key='jwt', value=token, httponly=True)
                    request.session['first_name'] = first_name
                    request.session['user_role'] = role
                    return response
                else:
                    messages.error(request, "Invalid email or password.")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'hide_header': True})

def profil(request):
    first_name = None
    last_name = None
    email = None

    if 'email' in request.session:
        email = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("SELECT first_name, last_name FROM users WHERE email = %s", [email])
            result = cursor.fetchone()
            if result:
                first_name, last_name = result

    return render(request, 'profil.html', {'first_name': first_name, 'last_name': last_name, 'email': email})

def logout(request):
    response = redirect('home')
    response.delete_cookie('jwt')
    del request.session['first_name']
    request.session.flush()
    return response


# === Product Management Views ===
def home(request):
    products = get_all_products()
    formatted_products = [
        {
            'id': p[0], 'name': p[1], 
            'description': p[2], 
            'price': p[3], 
            'image': 'assets/' + p[4],
            } for p in products
        ]
    return render(request, 'home.html', {'products': formatted_products, 'MEDIA_URL': settings.MEDIA_URL})

@admin_required
def admin_dashboard(request):
    products = get_all_products()
    formatted_products = [
        {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'image': product[4]
        } for product in products
    ]
    return render(request, 'admin_dashboard.html', {'products': formatted_products})

def product_detail(request, product_id):
    product_data = get_product_by_id(product_id)
    if product_data:
        product = {
            'id': product_data[0],
            'name': product_data[1],
            'description': product_data[2],
            'price': product_data[3],
            'image': 'assets/' + product_data[4]
        }
    return render(request, 'product_detail.html', {'product': product, 'MEDIA_URL': settings.MEDIA_URL})


def edit_product(request, product_id):
    product = get_product_by_id(product_id)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            update_product(product_id, name, description, price)
            return redirect('admin_dashboard')
    else:
        initial_data = {
            'name': product[1], # type: ignore
            'description': product[2], # type: ignore
            'price': product[3], # type: ignore
        }
        form = UpdateProductForm(initial=initial_data)

    return render(request, 'edit_product.html', {'form': form, 'product_id': product_id})
