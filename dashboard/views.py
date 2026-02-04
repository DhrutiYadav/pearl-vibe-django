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
from django.db.models import Count
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncYear
from django.db.models.functions import ExtractMonth

from datetime import timedelta
from collections import defaultdict
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Order   # change app name if your Order model is elsewhere

from store.forms import CustomerForm
from store.models import Customer

from store.forms import OrderSummaryForm
from store.models import OrderSummary

from store.forms import InvoiceForm
from store.models import Invoice

from store.forms import ShippingAddressForm

from django.contrib.auth.models import User
from store.forms import UserEditForm


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
    query = request.GET.get('q')

    orders = Order.objects.all().order_by('-date_ordered')

    if query:
        orders = orders.filter(
            Q(id__icontains=query) |
            Q(customer__name__icontains=query)
        )

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

    # 🏆 Top Selling Products
    top_products = OrderItem.objects.filter(order__complete=True) \
        .values('product__id', 'product__name', 'product__price') \
        .annotate(
        total_sold=Sum('quantity'),
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    ).order_by('-total_sold')[:10]

    # 📊 DATA FOR TOP SELLING PRODUCTS CHART
    product_names = [item['product__name'] for item in top_products]
    product_sales = [item['total_sold'] for item in top_products]

    # 📆 SALES THIS MONTH
    today = timezone.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    monthly_revenue = OrderItem.objects.filter(
        order__complete=True,
        order__date_ordered__gte=first_day_of_month
    ).aggregate(
        total=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    # 📈 SALES OVER LAST 7 DAYS
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    sales_data = OrderItem.objects.filter(
        order__complete=True,
        order__date_ordered__date__gte=seven_days_ago
    ).annotate(
        day=F('order__date_ordered__date')
    ).values('day').annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    ).order_by('day')

    # Fill missing days with 0 revenue
    sales_dict = defaultdict(int)
    for entry in sales_data:
        sales_dict[entry['day']] = float(entry['revenue'])

    dates = []
    revenues = []

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)
        dates.append(day.strftime("%d %b"))
        revenues.append(sales_dict.get(day, 0))

    # 🥧 SALES BY CATEGORY
    category_data = OrderItem.objects.filter(order__complete=True) \
        .values('product__subcategory__category__name') \
        .annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    ).order_by('-revenue')

    category_labels = [item['product__subcategory__category__name'] for item in category_data]
    category_revenues = [float(item['revenue']) for item in category_data]

    # 📅 MONTHLY SALES COMPARISON (Last 6 Months)
    today = timezone.now()
    six_months_ago = today - timedelta(days=180)

    monthly_data = OrderItem.objects.filter(
        order__complete=True,
        order__date_ordered__gte=six_months_ago
    ).annotate(
        month=TruncMonth('order__date_ordered')
    ).values('month').annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    ).order_by('month')

    month_labels = [entry['month'].strftime('%b %Y') for entry in monthly_data]
    month_revenues = [float(entry['revenue']) for entry in monthly_data]

    # 📆 YEARLY SALES COMPARISON
    yearly_data = OrderItem.objects.filter(order__complete=True) \
        .annotate(
        year=TruncYear('order__date_ordered')
    ).values('year').annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    ).order_by('year')

    year_labels = [entry['year'].strftime('%Y') for entry in yearly_data]
    year_revenues = [float(entry['revenue']) for entry in yearly_data]

    # 📅 MONTHLY SALES (JAN–DEC FOR CURRENT YEAR)
    selected_year = request.GET.get('year')

    if selected_year:
        selected_year = int(selected_year)
    else:
        selected_year = timezone.now().year

    monthly_sales = OrderItem.objects.filter(
        order__complete=True,
        order__date_ordered__year=selected_year
    ).annotate(
        month=ExtractMonth('order__date_ordered')
    ).values('month').annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    )

    # Convert to dictionary {month_number: revenue}
    sales_dict = {entry['month']: float(entry['revenue']) for entry in monthly_sales}

    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    month_revenues = [sales_dict.get(i, 0) for i in range(1, 13)]

    # 📈 REVENUE vs ORDERS TREND (Last 7 Days)
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    orders_data = Order.objects.filter(
        complete=True,
        date_ordered__date__gte=seven_days_ago
    ).values('date_ordered__date').annotate(
        order_count=Count('id')
    ).order_by('date_ordered__date')

    revenue_data = OrderItem.objects.filter(
        order__complete=True,
        order__date_ordered__date__gte=seven_days_ago
    ).annotate(
        day=F('order__date_ordered__date')
    ).values('day').annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    )

    orders_dict = {entry['date_ordered__date']: entry['order_count'] for entry in orders_data}
    revenue_dict = {entry['day']: float(entry['revenue']) for entry in revenue_data}

    trend_dates = []
    trend_orders = []
    trend_revenue = []

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)
        trend_dates.append(day.strftime("%d %b"))
        trend_orders.append(orders_dict.get(day, 0))
        trend_revenue.append(revenue_dict.get(day, 0))

    # 💰 REVENUE BY PRICE RANGE
    price_ranges = {
        "Under ₹500": OrderItem.objects.filter(
            order__complete=True,
            product__price__lt=500
        ),
        "₹500 - ₹1000": OrderItem.objects.filter(
            order__complete=True,
            product__price__gte=500,
            product__price__lte=1000
        ),
        "Above ₹1000": OrderItem.objects.filter(
            order__complete=True,
            product__price__gt=1000
        ),
    }

    range_labels = []
    range_revenues = []

    for label, queryset in price_ranges.items():
        revenue = queryset.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('product__price') * F('quantity'),
                    output_field=DecimalField()
                )
            )
        )['total'] or 0

        range_labels.append(label)
        range_revenues.append(float(revenue))

        # 💳 AVERAGE ORDER VALUE (AOV) TREND – Last 7 Days
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=6)

        # Orders per day
        orders_per_day = Order.objects.filter(
            complete=True,
            date_ordered__date__gte=seven_days_ago
        ).values('date_ordered__date').annotate(
            count=Count('id')
        )

        # Revenue per day
        revenue_per_day = OrderItem.objects.filter(
            order__complete=True,
            order__date_ordered__date__gte=seven_days_ago
        ).annotate(
            day=F('order__date_ordered__date')
        ).values('day').annotate(
            revenue=Sum(
                ExpressionWrapper(
                    F('product__price') * F('quantity'),
                    output_field=DecimalField()
                )
            )
        )

        orders_dict = {entry['date_ordered__date']: entry['count'] for entry in orders_per_day}
        revenue_dict = {entry['day']: float(entry['revenue']) for entry in revenue_per_day}

        aov_dates = []
        aov_values = []

        for i in range(7):
            day = seven_days_ago + timedelta(days=i)
            orders = orders_dict.get(day, 0)
            revenue = revenue_dict.get(day, 0)

            aov = revenue / orders if orders > 0 else 0

            aov_dates.append(day.strftime("%d %b"))
            aov_values.append(round(aov, 2))

    # 💎 CUSTOMER LIFETIME VALUE (CLV)

    customer_clv = OrderItem.objects.filter(order__complete=True) \
        .values(
        'order__customer__id',
        'order__customer__user__username'
    ).annotate(
        total_spent=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        ),
        total_orders=Count('order', distinct=True)
    ).order_by('-total_spent')[:10]  # Top 10 customers

    # 📊 CLV CHART DATA (Top 5 Customers)
    top_customers = list(customer_clv[:5])

    clv_labels = [c['order__customer__user__username'] for c in top_customers]
    clv_values = [float(c['total_spent']) for c in top_customers]

    context = {
        'total_orders': total_orders,
        'paid_orders': paid_orders,
        'unpaid_orders': unpaid_orders,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'sales_dates': dates,
        'sales_revenues': revenues,
        'chart_product_names': product_names,
        'chart_product_sales': product_sales,
        'category_labels': category_labels,
        'category_revenues': category_revenues,
        'month_labels': month_labels,
        'month_revenues': month_revenues,
        'year_labels': year_labels,
        'year_revenues': year_revenues,
        'year_month_labels': month_labels,
        'year_month_revenues': month_revenues,
        # 'current_year': current_year,
        'year_month_labels': month_labels,
        'year_month_revenues': month_revenues,
        'selected_year': selected_year,
        'available_years': range(timezone.now().year, timezone.now().year - 5, -1),
        'revenue_orders_dates': trend_dates,
        'revenue_orders_counts': trend_orders,
        'revenue_orders_revenue': trend_revenue,
        'price_range_labels': range_labels,
        'price_range_revenues': range_revenues,
        'aov_dates': aov_dates,
        'aov_values': aov_values,
        'customer_clv': customer_clv,
        'clv_labels': clv_labels,
        'clv_values': clv_values,

    }

    return render(request, 'dashboard/reports.html', context)


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.complete = request.POST.get('complete') == 'true'
        order.save()
        return redirect('dashboard:orders')

    return render(request, 'dashboard/edit_order.html', {'order': order})


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('dashboard:orders')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_customers')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'dashboard/edit_customer.html', {'form': form})


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect('dashboard:dashboard_customers')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def edit_order_summary(request, summary_id):
    summary = get_object_or_404(OrderSummary, id=summary_id)

    if request.method == 'POST':
        form = OrderSummaryForm(request.POST, instance=summary)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_order_summaries')
    else:
        form = OrderSummaryForm(instance=summary)

    return render(request, 'dashboard/edit_order_summary.html', {'form': form})


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_invoices')
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'dashboard/edit_invoice.html', {'form': form})

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return redirect('dashboard:dashboard_invoices')


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def edit_shipping_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard_shipping_addresses')
    else:
        form = ShippingAddressForm(instance=address)

    return render(request, 'dashboard/edit_shipping_address.html', {'form': form})

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def delete_shipping_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id)
    address.delete()
    return redirect('dashboard:dashboard_shipping_addresses')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:users')
    else:
        form = UserEditForm(instance=user_obj)

    return render(request, 'dashboard/edit_user.html', {'form': form})


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    # prevent deleting yourself (important safety)
    if request.user == user_obj:
        messages.error(request, "You cannot delete your own account.")
        return redirect('dashboard:users')

    user_obj.delete()
    return redirect('dashboard:users')
