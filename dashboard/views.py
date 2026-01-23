from django.contrib.auth.decorators import login_required, user_passes_test
from store.models import SubCategory
from django.shortcuts import get_object_or_404, redirect, render
from store.forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test
from store.models import Product, Category
from store.forms import CategoryForm
from django.contrib.auth.models import User
from store.forms import SubCategoryForm
from store.models import Order

def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Edit Product'
    })



# admin/staff check
def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_home(request):
    return render(request, 'dashboard/home.html')


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_products(request):
    products = Product.objects.all()
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
            form.save()
            return redirect('dashboard_products')
    else:
        form = ProductForm()

    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_subcategories(request):
    subcategories = SubCategory.objects.all()  # Fetch all subcategories
    return render(request, 'dashboard/subcategories.html', {
        'subcategories': subcategories
    })

@login_required(login_url='/admin/login/')
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
        return redirect('dashboard_products')

    # optional safety fallback
    return redirect('dashboard_products')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def dashboard_add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_categories')

    return render(request, 'dashboard/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


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
            return redirect('dashboard_subcategories')
    else:
        form = SubCategoryForm()

    return render(request, 'dashboard/subcategory_form.html', {
        'form': form
    })

# FILE: dashboard/views.py

from django.shortcuts import render
from store.models import Order   # Order model is in store app

def dashboard_home(request):
    return render(request, 'dashboard/home.html')


def dashboard_orders(request):
    orders = Order.objects.all().order_by('-date_ordered')

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)
