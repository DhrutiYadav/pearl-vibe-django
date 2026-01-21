from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .utils import cookieCart
import json
import datetime


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def dashboard_home(request):
    context = {
        "total_products": 120,
        "total_orders": 45,
        "total_users": 20,
        "revenue": 56000,
    }
    return render(request, "dashboard/dashboard.html", context)


# ---------------------------
# STORE / PRODUCT VIEWS
# ---------------------------

def store(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def subcategories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'store/subcategories.html', {
        'category': category,
        'subcategories': subcategories
    })


def products_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    products = subcategory.products.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'subcategory': subcategory
    })


# ---------------------------
# AUTH VIEWS
# ---------------------------

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please provide username and password.')
            return redirect('store:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('store:register')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Customer.objects.create(
            user=user,
            name=username
        )

        messages.success(request, 'Account created! Please log in.')
        return redirect('store:login')

    return render(request, 'store/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('store:home')


# ---------------------------
# CART & CHECKOUT
# ---------------------------

def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username}
        )

        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return render(request, 'store/cart.html', {
        'items': items,
        'order': order,
        'cartItems': cartItems
    })


def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username}
        )

        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return render(request, 'store/checkout.html', {
        'items': items,
        'order': order,
        'cartItems': cartItems
    })


# def updateItem(request):
#     data = json.loads(request.body)
#
#     productId = data['productId']
#     action = data['action']
#
#     # ✅ NEW: get size & color from request
#     size = data.get('size')
#     color = data.get('color')
#
#     customer = request.user.customer
#     product = Product.objects.get(id=productId)
#
#     order, created = Order.objects.get_or_create(
#         customer=customer,
#         complete=False
#     )
#
#     # ✅ IMPORTANT: include size & color here
#     orderItem, created = OrderItem.objects.get_or_create(
#         order=order,
#         product=product,
#         size=size,
#         color=color,
#     )
#
#     if action == 'add':
#         orderItem.quantity += 1
#         orderItem.save()
#     elif action == 'remove':
#         orderItem.quantity -= 1
#
#         if orderItem.quantity <= 0:
#             orderItem.delete()
#         else:
#             orderItem.save()
#
#
#     elif action == 'delete':
#         orderItem.delete()
#         return JsonResponse('Item deleted', safe=False)
#
#     return JsonResponse('Item updated', safe=False)

def updateItem(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']

    # get size & color
    size = data.get('size')
    color = data.get('color')

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False
    )

    # IMPORTANT: include size & color
    orderItem, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        size=size,
        color=color,
    )

    # 🔥 VERY IMPORTANT FIX
    # If new row created, start quantity at 0
    if created:
        orderItem.quantity = 0

    if action == 'add':
        orderItem.quantity += 1
        orderItem.save()

    elif action == 'remove':
        orderItem.quantity -= 1

        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()

    elif action == 'delete':
        orderItem.delete()

    return JsonResponse('Item updated', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment submitted', safe=False)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })
