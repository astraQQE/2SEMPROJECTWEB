from django import forms
from .models import Product,User
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'brand', 'stock', 'image']

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('buyer', 'Покупатель'),
        ('admin', 'Администратор'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']