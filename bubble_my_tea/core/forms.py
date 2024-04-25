from django import forms
from django.core.exceptions import ValidationError
from django.db import connection

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-transparent focus:border-blue-500 rounded', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-transparent focus:border-blue-500 rounded', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-blue-500 rounded', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-transparent focus:border-blue-500 rounded', 'placeholder': 'Enter Password'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.email_exists(email):
            raise ValidationError("A user with that email already exists.")
        return email

    def email_exists(self, email):
        """Check if an email already exists in the database."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email = %s", [email])
            return cursor.fetchone() is not None

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-transparent focus:border-blue-500 rounded', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'px-4 py-3 bg-gray-100 w-full text-sm outline-none border-b-2 border-transparent focus:border-blue-500 rounded', 'placeholder': 'Password'}))
    
    
class UpdateProductForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control '}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['image'].required = False

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0: # type: ignore
            raise ValidationError("The price must be greater than zero.")
        return price
