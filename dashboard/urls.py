# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('orders/', views.dashboard_orders, name='dashboard_orders'),
    path('users/', views.dashboard_users, name='dashboard_users'),
]
