from django.urls import path
from . import views

app_name = 'dashboard'   # 🔥 THIS LINE IS REQUIRED

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('products/add/', views.dashboard_add_product, name='dashboard_add_product'),
    path('products/edit/<int:pk>/', views.dashboard_edit_product, name='dashboard_edit_product'),
    path('products/delete/<int:pk>/', views.dashboard_delete_product, name='dashboard_delete_product'),


    # path('users/', views.dashboard_users, name='dashboard_users'),
    path('categories/', views.dashboard_categories, name='dashboard_categories'),
    path('categories/add/', views.dashboard_add_category, name='dashboard_add_category'),
    path('categories/edit/<int:pk>/', views.dashboard_edit_category, name='dashboard_edit_category'),

    path('categories/delete/<int:pk>/', views.dashboard_delete_category, name='dashboard_delete_category'),

    path('orders/', views.dashboard_orders, name='orders'),


    path('subcategories/', views.dashboard_subcategories, name='dashboard_subcategories'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategories/edit/<int:pk>/', views.edit_subcategory, name='edit_subcategory'),
    path("subcategory/delete/<int:pk>/", views.delete_subcategory, name="delete_subcategory"),
    path('users/', views.users_list, name='users'),

    path('customers/', views.dashboard_customers, name='dashboard_customers'),
    path('shipping-addresses/', views.dashboard_shipping_addresses, name='dashboard_shipping_addresses'),
    path('order-summaries/', views.dashboard_order_summaries, name='dashboard_order_summaries'),
    path('invoices/', views.dashboard_invoices, name='dashboard_invoices'),
    path('reports/', views.reports_dashboard, name='reports_dashboard'),

]
