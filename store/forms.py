from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['subcategory', 'name', 'price', 'image', 'description']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
