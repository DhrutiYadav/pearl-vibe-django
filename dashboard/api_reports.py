# dashboard/api_reports.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from collections import defaultdict

from store.models import Order, OrderItem


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def sales_report_api(request):

    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    sales_queryset = OrderItem.objects.filter(
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

    sales_dict = defaultdict(float)

    for entry in sales_queryset:
        sales_dict[entry['day']] = float(entry['revenue'] or 0)

    labels = []
    revenues = []

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)
        labels.append(day.strftime("%d %b"))
        revenues.append(sales_dict.get(day, 0))

    return JsonResponse({
        "labels": labels,
        "revenues": revenues
    })