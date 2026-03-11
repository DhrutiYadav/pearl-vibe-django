# dashboard/api_reports.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from collections import defaultdict

from store.models import Order, OrderItem


def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def sales_report_api(request):

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    query = OrderItem.objects.filter(order__complete=True)

    range_filter = request.GET.get("range")

    if range_filter == "today":
        start_date = today
        end_date = today

    elif range_filter == "week":
        start_date = today - timedelta(days=6)
        end_date = today

    elif range_filter == "month":
        start_date = today.replace(day=1)
        end_date = today

    elif from_date and to_date:
        start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    else:
        start_date = seven_days_ago
        end_date = today

    query = query.filter(
        order__date_ordered__date__range=[start_date, end_date]
    )

    sales_queryset = query.annotate(
        day=F('order__date_ordered__date')
    ).values('day').annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('product__price') * F('quantity'),
                output_field=DecimalField()
            )
        )
    ).order_by('day')

    sales_dict = defaultdict(float)

    for entry in sales_queryset:
        sales_dict[entry['day']] = float(entry['revenue'] or 0)

    labels = []
    revenues = []

    current_day = start_date

    while current_day <= end_date:
        labels.append(current_day.strftime("%d %b"))
        revenues.append(sales_dict.get(current_day, 0))
        current_day += timedelta(days=1)

    return JsonResponse({
        "labels": labels,
        "revenues": revenues
    })


@login_required
@user_passes_test(is_admin)
def daywise_report_api(request):

    month = request.GET.get("month")
    year = request.GET.get("year")

    if not month or not year:
        return JsonResponse({
            "labels": [],
            "orders": [],
            "revenues": []
        })

    month = int(month)
    year = int(year)

    query = OrderItem.objects.filter(
        order__complete=True,
        order__date_ordered__year=year,
        order__date_ordered__month=month
    )

    sales_queryset = query.annotate(
        day=F("order__date_ordered__day")
    ).values("day").annotate(
        orders=Count("order", distinct=True),
        revenue=Sum(
            ExpressionWrapper(
                F("product__price") * F("quantity"),
                output_field=DecimalField()
            )
        )
    ).order_by("day")

    sales_dict = defaultdict(lambda: {"orders": 0, "revenue": 0})

    for entry in sales_queryset:
        sales_dict[entry["day"]] = {
            "orders": entry["orders"] or 0,
            "revenue": float(entry["revenue"] or 0)
        }

    labels = []
    orders = []
    revenues = []

    for day in range(1, 32):
        labels.append(day)
        orders.append(sales_dict[day]["orders"])
        revenues.append(sales_dict[day]["revenue"])

    return JsonResponse({
        "labels": labels,
        "orders": orders,
        "revenues": revenues
    })

@login_required
@user_passes_test(is_admin)
def monthly_sales_api(request):

    year = request.GET.get("year")

    if not year:
        return JsonResponse({
            "labels": [],
            "revenues": []
        })

    year = int(year)

    data = (
        OrderItem.objects
        .filter(order__complete=True, order__date_ordered__year=year)
        .annotate(month=F("order__date_ordered__month"))
        .values("month")
        .annotate(
            revenue=Sum(
                ExpressionWrapper(
                    F("product__price") * F("quantity"),
                    output_field=DecimalField()
                )
            )
        )
        .order_by("month")
    )

    revenue_dict = defaultdict(float)

    for item in data:
        revenue_dict[item["month"]] = float(item["revenue"] or 0)

    labels = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    revenues = []

    for i in range(1,13):
        revenues.append(revenue_dict.get(i,0))

    return JsonResponse({
        "labels": labels,
        "revenues": revenues
    })

@login_required
@user_passes_test(is_admin)
def category_report_api(request):

    from django.db.models import Sum
    from store.models import OrderItem

    categories = (
        OrderItem.objects.filter(order__complete=True)
        .values("product__subcategory__category__name")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("-revenue")
    )

    labels = []
    revenues = []

    for c in categories:
        labels.append(c["product__subcategory__category__name"])
        revenues.append(float(c["revenue"] or 0))

    return JsonResponse({
        "labels": labels,
        "revenues": revenues
    })

def top_products_api(request):

    from django.db.models import Sum
    from store.models import OrderItem
    from django.http import JsonResponse

    products = (
        OrderItem.objects
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:10]
    )

    labels = []
    data = []

    for p in products:
        labels.append(p["product__name"])
        data.append(p["total_sold"])

    return JsonResponse({
        "labels": labels,
        "data": data
    })