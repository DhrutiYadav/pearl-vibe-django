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
import uuid
from .models import OrderSummary, Invoice
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.db.models import Q, Sum


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .forms import RegisterForm

font_path = os.path.join(settings.BASE_DIR, 'static/fonts/DejaVuSans.ttf')
pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))


def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")

        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password changed successfully")
            return redirect("store:login")
        else:
            messages.error(request, "Old password is incorrect")

    return render(request, "store/change_password.html")

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
    query = request.GET.get('q')  # get search text

    all_products = Product.objects.all()
    search_results = None

    if query:
        search_results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # 🔥 Top Selling Products (only from completed orders)
    top_products = Product.objects.filter(orderitem__order__complete=True) \
        .annotate(total_sold=Sum('orderitem__quantity')) \
        .order_by('-total_sold')[:8]

    context = {
        'products': all_products,
        'top_products': top_products,
        'search_results': search_results,
        'search_query': query,
    }
    return render(request, 'store/product_list.html', context)


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

def search_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
        )[:5]

        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
            })

    return JsonResponse(results, safe=False)


# ---------------------------
# AUTH VIEWS
# ---------------------------


SECURITY_QUESTIONS = [
    ("website", "Which is the website you frequently visit?"),
    ("school", "What is the name of your first school?"),
    ("color", "What is your favourite colour?"),
    ("vehicle", "What is the registration number of your first vehicle?"),
    ("book", "Which is your favourite book?"),
    ("sport", "What is your favourite sport?"),
    ("birth", "What is your place of birth?"),
]
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('store:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


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

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)

            # 🔥 SAFE WAY
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={"name": user.username}
            )

            if not customer.security_question:
                messages.error(request, "Security question not set. Contact support.")
                return redirect("store:forgot_password")

            return render(request, "store/security_question.html", {
                "user_id": user.id,
                "question": customer.get_security_question_display()
            })

        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "store/forgot_password.html")

def reset_password(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        answer = request.POST.get("answer")
        new_password = request.POST.get("new_password")

        user = User.objects.get(id=user_id)
        customer = user.customer

        if customer.security_answer.lower() == answer.lower():
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password reset successful! Please login.")
            return redirect("store:login")
        else:
            messages.error(request, "Wrong security answer")

    return redirect("store:forgot_password")

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


def updateItem(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']

    # get size & color
    size = data.get('size') or None
    color = data.get('color') or None

    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.username, 'email': request.user.email}
    )

    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False
    )

    # Try to get item first
    orderItem = OrderItem.objects.filter(
        order=order,
        product=product,
        size=size,
        color=color,
    ).first()

    # DELETE should not create new row
    if action == 'delete':
        if orderItem:
            orderItem.delete()
        return JsonResponse('Item deleted', safe=False)

    # For add/remove, create if missing
    if not orderItem:
        orderItem = OrderItem.objects.create(
            order=order,
            product=product,
            size=size,
            color=color,
            quantity=0
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
    data = json.loads(request.body or '{}')

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username, 'email': request.user.email}
        )

        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        order.transaction_id = transaction_id

        # ✅ Payment already confirmed by PayPal
        order.complete = True
        order.save()

        # -------------------------
        # CREATE ORDER SUMMARY
        # -------------------------
        subtotal = order.get_cart_total
        tax = subtotal * 0.05
        shipping_cost = 50 if order.shipping else 0
        grand_total = subtotal + tax + shipping_cost

        OrderSummary.objects.update_or_create(
            order=order,
            defaults={
                "subtotal": subtotal,
                "tax": tax,
                "shipping_cost": shipping_cost,
                "total": grand_total
            }
        )

        # -------------------------
        # CREATE INVOICE
        # -------------------------
        Invoice.objects.get_or_create(
            order=order,
            defaults={
                "invoice_number": f"PV-{uuid.uuid4().hex[:8].upper()}"
            }
        )

        if order.shipping and 'shipping' in data:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping'].get('address', ''),
                city=data['shipping'].get('city', ''),
                state=data['shipping'].get('state', ''),
                zipcode=data['shipping'].get('zipcode', ''),
            )

    print("ORDER SAVED:", order.id, "COMPLETE:", order.complete)
    return JsonResponse({'order_id': order.id if order else 0}, safe=False)



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    summary = getattr(order, "summary", None)
    invoice = getattr(order, "invoice", None)

    return render(request, 'store/order_success.html', {
        'order': order,
        'summary': summary,
        'invoice': invoice
    })


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access them
    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.BASE_DIR, uri.replace(settings.STATIC_URL, "static/"))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.BASE_DIR, uri.replace(settings.MEDIA_URL, "media/"))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception('Media URI must start with STATIC_URL or MEDIA_URL')
    return path

def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    summary = order.summary
    invoice = order.invoice
    items = order.orderitem_set.all()

    template = get_template('store/invoice_pdf.html')
    html = template.render({
        'order': order,
        'summary': summary,
        'invoice': invoice,
        'items': items,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'

    pisa.CreatePDF(
        html,
        dest=response,
        encoding='utf-8',
        link_callback=link_callback  # 👈 THIS is the fix
    )

    return response


from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer, complete=True).order_by('-date_ordered')

    return render(request, 'store/order_history.html', {
        'orders': orders
    })
