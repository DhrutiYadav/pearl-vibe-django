from django.contrib.auth.decorators import login_required, user_passes_test
from store.models import SubCategory
from django.shortcuts import get_object_or_404, redirect, render
from store.forms import ProductForm
from store.models import Product, Category
from store.forms import CategoryForm
from django.contrib.auth.models import User
from store.forms import SubCategoryForm
from django.contrib import messages
import json
from store.models import Customer, Invoice, OrderSummary, ShippingAddress

from django.shortcuts import render
from store.models import Order, OrderItem
from django.db.models import Sum, Count
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from django.utils import timezone
from datetime import timedelta


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

            # 🔥 GET COLORS FROM HIDDEN INPUT
            colors_json = request.POST.get("colors", "[]")

            try:
                product.colors = json.loads(colors_json)  # convert JSON string → Python list
            except json.JSONDecodeError:
                product.colors = []

            product.save()
            form.save_m2m()

            return redirect('dashboard:dashboard_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Edit Product',
        'existing_colors': json.dumps(product.colors or [])

    })


# admin/staff check
def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_products(request):
    products = Product.objects.select_related('subcategory')

    for product in products:
        if not product.sizes:
            product.size_list = []

        # If sizes is already a list (best case)
        elif isinstance(product.sizes, list):
            product.size_list = product.sizes

        # If sizes is a JSON string like '["L", "XL"]'
        elif isinstance(product.sizes, str):
            try:
                product.size_list = json.loads(product.sizes)
            except json.JSONDecodeError:
                product.size_list = []

        else:
            product.size_list = []

    return render(request, 'dashboard/products.html', {
        'products': products
    })

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_users(request):
    return render(request, 'dashboard/users.html')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            colors_json = request.POST.get("colors", "[]")
            try:
                product.colors = json.loads(colors_json)
            except json.JSONDecodeError:
                product.colors = []

            product.save()
            form.save_m2m()
            return redirect('dashboard:dashboard_products')

    else:
        form = ProductForm()

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Add Product',
        'existing_colors': '[]'  # 🔥 ADD THIS LINE
    })


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_subcategories(request):
    subcategories = SubCategory.objects.all()  # Fetch all subcategories
    return render(request, 'dashboard/subcategories.html', {
        'subcategories': subcategories
    })

@login_required(login_url='/admain/login/')
@user_passes_test(is_admin)
def dashboard_categories(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'dashboard/categories.html', {
        'categories': categories
    })


# EDIT product
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product'})

# DELETE product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:dashboard_products')

    # optional safety fallback
    return redirect('dashboard:dashboard_products')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_categories')

    return render(request, 'dashboard/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })
def dashboard_edit_category(request, pk):
    category = Category.objects.get(pk=pk)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_categories')

    return render(request, 'dashboard/category_form.html', {'form': form})



@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_home(request):
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_subcategories': SubCategory.objects.count(),
        'total_users': User.objects.count(),
    }
    return render(request, 'dashboard/home.html', context)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def add_subcategory(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_subcategories')
    else:
        form = SubCategoryForm()

    return render(request, 'dashboard/subcategory_form.html', {
        'form': form
    })


def dashboard_orders(request):
    orders = Order.objects.all().order_by('-date_ordered')

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)


@login_required
@user_passes_test(is_admin)
def users_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)

    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_subcategories')
    else:
        form = SubCategoryForm(instance=subcategory)

    return render(request, 'dashboard/subcategory_form.html', {'form': form})

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('dashboard:dashboard_categories')

    return render(request, 'dashboard/category_confirm_delete.html', {
        'category': category
    })


@login_required
@user_passes_test(is_admin)
def delete_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)

    if request.method == "POST":
        subcategory.delete()
        messages.success(request, "Subcategory deleted successfully.")
        return redirect("dashboard:dashboard_subcategories")

    return render(request, "dashboard/delete_subcategory.html", {"subcategory": subcategory})

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_customers(request):
    customers = Customer.objects.select_related('user').all()

    return render(request, 'dashboard/customers.html', {
        'customers': customers
    })

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_shipping_addresses(request):
    addresses = ShippingAddress.objects.select_related('customer', 'order').all()

    return render(request, 'dashboard/shipping_addresses.html', {
        'addresses': addresses
    })

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_order_summaries(request):
    summaries = OrderSummary.objects.select_related('order').all()

    return render(request, 'dashboard/order_summaries.html', {
        'summaries': summaries
    })

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_invoices(request):
    invoices = Invoice.objects.select_related('order').all()

    return render(request, 'dashboard/invoices.html', {
        'invoices': invoices
    })

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def reports_dashboard(request):

    total_orders = Order.objects.count()

    # ✅ USE complete INSTEAD OF paid
    paid_orders = Order.objects.filter(complete=True).count()
    unpaid_orders = Order.objects.filter(complete=False).count()

    # 💰 Revenue = sum of (product price × quantity) for completed orders
    total_revenue = OrderItem.objects.filter(
        order__complete=True
    ).aggregate(
        total=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    # ✅ Your model uses date_ordered, not created_at
    recent_orders = Order.objects.select_related('customer__user').order_by('-date_ordered')[:10]

    context = {
        'total_orders': total_orders,
        'paid_orders': paid_orders,
        'unpaid_orders': unpaid_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard/reports.html', context)