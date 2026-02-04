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
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),



    path('subcategories/', views.dashboard_subcategories, name='dashboard_subcategories'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategories/edit/<int:pk>/', views.edit_subcategory, name='edit_subcategory'),
    path("subcategory/delete/<int:pk>/", views.delete_subcategory, name="delete_subcategory"),

    path('users/', views.users_list, name='users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),


    path('customers/', views.dashboard_customers, name='dashboard_customers'),
    path('customers/edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    path('shipping-addresses/', views.dashboard_shipping_addresses, name='dashboard_shipping_addresses'),
    path('shipping-addresses/edit/<int:address_id>/', views.edit_shipping_address, name='edit_shipping_address'),
    path('shipping-addresses/delete/<int:address_id>/', views.delete_shipping_address, name='delete_shipping_address'),



    path('order-summaries/', views.dashboard_order_summaries, name='dashboard_order_summaries'),
    path('order-summaries/edit/<int:summary_id>/', views.edit_order_summary, name='edit_order_summary'),


    path('invoices/', views.dashboard_invoices, name='dashboard_invoices'),
    path('invoices/edit/<int:invoice_id>/', views.edit_invoice, name='edit_invoice'),
    path('invoices/delete/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),



    path('reports/', views.reports_dashboard, name='reports_dashboard'),

]
