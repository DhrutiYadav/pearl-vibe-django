from django import forms
from .models import Product, Category, SubCategory
from store.models import Customer
from store.models import OrderSummary

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['subcategory', 'name', 'price', 'image', 'description']

class ProductForm(forms.ModelForm):
    # Hidden field that will receive colors from JS
    colors = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Product
        fields = ['subcategory', 'name', 'price', 'image', 'description', 'sizes', 'colors']

    def clean_colors(self):
        """
        Convert comma-separated string from hidden input
        into a Python list for the JSONField
        """
        colors = self.cleaned_data.get('colors')

        if colors:
            return [c.strip() for c in colors.split(',') if c.strip()]

        return []

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'image']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']

class OrderSummaryForm(forms.ModelForm):
     class Meta:
        model = OrderSummary
        fields = ['subtotal', 'tax', 'shipping_cost', 'total']  # adjust fields based on your model