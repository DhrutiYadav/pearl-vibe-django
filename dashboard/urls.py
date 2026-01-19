from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('products/add/', views.dashboard_add_product, name='dashboard_add_product'),
    path('products/edit/<int:pk>/', views.dashboard_edit_product, name='dashboard_edit_product'),
    path('products/delete/<int:pk>/', views.dashboard_delete_product, name='dashboard_delete_product'),

    path('orders/', views.dashboard_orders, name='dashboard_orders'),
    path('users/', views.dashboard_users, name='dashboard_users'),
    path('subcategories/', views.dashboard_subcategories, name='dashboard_subcategories'),
    path('categories/', views.dashboard_categories, name='dashboard_categories'),
    path('categories/add/', views.dashboard_add_category, name='dashboard_add_category'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),

]
