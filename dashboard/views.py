from django.shortcuts import render
from django.http import HttpResponse

def dashboard_home(request):
    return render(request, 'dashboard/home.html')

def dashboard_products(request):
    return render(request, 'dashboard/products.html')

def dashboard_orders(request):
    return render(request, 'dashboard/orders.html')

def dashboard_users(request):
    return render(request, 'dashboard/users.html')
