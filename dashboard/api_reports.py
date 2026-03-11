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

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    query = OrderItem.objects.filter(order__complete=True)

    if from_date and to_date:
        query = query.filter(
            order__date_ordered__date__range=[from_date, to_date]
        )
    else:
        query = query.filter(
            order__date_ordered__date__gte=seven_days_ago
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

    # determine range
    if from_date and to_date:
        start_date = timezone.datetime.strptime(from_date, "%Y-%m-%d").date()
        end_date = timezone.datetime.strptime(to_date, "%Y-%m-%d").date()
    else:
        start_date = seven_days_ago
        end_date = today

    current_day = start_date

    while current_day <= end_date:
        labels.append(current_day.strftime("%d %b"))
        revenues.append(sales_dict.get(current_day, 0))
        current_day += timedelta(days=1)

    return JsonResponse({
        "labels": labels,
        "revenues": revenues
    })