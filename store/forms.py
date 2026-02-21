from django import forms
from .models import Product, Category, SubCategory
from store.models import Customer
from store.models import OrderSummary
from store.models import Invoice
from store.models import ShippingAddress
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_no = forms.CharField(max_length=15, required=True)
    country = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)

    security_question = forms.CharField(max_length=255, required=True)
    security_answer = forms.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "contact_no",
            "country",
            "address",
            "security_question",
            "security_answer",
            "password1",
            "password2"
        ]

    def save(self, commit=True):
        user = super().save(commit)

        Customer.objects.create(
            user=user,
            name=user.username,
            email=self.cleaned_data["email"],
            contact_no=self.cleaned_data["contact_no"],
            country=self.cleaned_data["country"],
            address=self.cleaned_data["address"],

            security_question=self.cleaned_data["security_question"],
            security_answer=self.cleaned_data["security_answer"],
        )
        return user

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

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'paid']


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active']

