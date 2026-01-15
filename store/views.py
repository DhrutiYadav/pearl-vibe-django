# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Category, SubCategory, Product
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from types import SimpleNamespace
# from django.http import JsonResponse
#
# def store(request):
#     products = Product.objects.all()
#     return render(request, 'store/product_list.html', {'products': products})
#
# def subcategories(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     subcategories = category.subcategories.all()
#     return render(request, 'store/subcategories.html', {'category': category, 'subcategories': subcategories})
#
# def products_by_subcategory(request, subcategory_id):
#     subcategory = get_object_or_404(SubCategory, id=subcategory_id)
#     products = subcategory.products.all()
#     return render(request, 'store/product_list.html', {'products': products, 'subcategory': subcategory})
#
# def register_view(request):
#     if request.method == 'POST':
#         from django.contrib.auth.models import User
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         if username and password:
#             User.objects.create_user(username=username, password=password)
#             messages.success(request, 'Account created, please log in.')
#             return redirect('store:login')
#     return render(request, 'store/register.html')
#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('store:home')
#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'store/login.html')
#
# def logout_view(request):
#     logout(request)
#     return redirect('store:home')
#
# # Cart & Checkout simple mock flow
# def cart_view(request):
#     # Build mock items list and order object used by your checkout template
#     items = []
#     products = Product.objects.all()[:3]
#     for p in products:
#         prod = SimpleNamespace(name=p.name, price=p.price, imageURL=p.imageURL)
#         item = SimpleNamespace(product=prod, quantity=1, subtotal=p.price)
#         items.append(item)
#     order = SimpleNamespace(get_cart_items=len(items), get_cart_total=sum([it.subtotal for it in items]), shipping=True)
#     return render(request, 'store/cart.html', {'items': items, 'order': order})
#
# def checkout_view(request):
#     # same mock data
#     items = []
#     products = Product.objects.all()[:3]
#     for p in products:
#         prod = SimpleNamespace(name=p.name, price=p.price, imageURL=p.imageURL)
#         item = SimpleNamespace(product=prod, quantity=1, subtotal=p.price)
#         items.append(item)
#     order = SimpleNamespace(get_cart_items=len(items), get_cart_total=sum([it.subtotal for it in items]), shipping=True)
#     return render(request, 'store/checkout.html', {'items': items, 'order': order})
#
# def process_order(request):
#     if request.method == 'POST':
#         # Accept JSON and respond success. In real app save order to DB.
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'invalid method'}, status=400)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from types import SimpleNamespace
from .models import Category, SubCategory, Product
from django.contrib.auth.models import User


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
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, 'Account created! Please log in.')
                return redirect('store:login')
        else:
            messages.error(request, 'Please provide username and password.')
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
            messages.error(request, 'Invalid credentials')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('store:home')


# ---------------------------
# CART & CHECKOUT MOCK FLOW
# ---------------------------

def cart_view(request):
    items = []
    products = Product.objects.all()[:3]
    for p in products:
        prod = SimpleNamespace(name=p.name, price=p.price, imageURL=p.imageURL)
        item = SimpleNamespace(product=prod, quantity=1, subtotal=p.price)
        items.append(item)

    order = SimpleNamespace(
        get_cart_items=len(items),
        get_cart_total=sum([it.subtotal for it in items]),
        shipping=True
    )
    return render(request, 'store/cart.html', {'items': items, 'order': order})


def checkout_view(request):
    items = []
    products = Product.objects.all()[:3]
    for p in products:
        prod = SimpleNamespace(name=p.name, price=p.price, imageURL=p.imageURL)
        item = SimpleNamespace(product=prod, quantity=1, subtotal=p.price)
        items.append(item)

    order = SimpleNamespace(
        get_cart_items=len(items),
        get_cart_total=sum([it.subtotal for it in items]),
        shipping=True
    )
    return render(request, 'store/checkout.html', {'items': items, 'order': order})


def process_order(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid method'}, status=400)
