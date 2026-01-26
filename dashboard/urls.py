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
    path('orders/', views.dashboard_orders, name='orders'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),

    path('subcategories/', views.dashboard_subcategories, name='dashboard_subcategories'),
    path('subcategories/edit/<int:pk>/', views.edit_subcategory, name='edit_subcategory'),
    path('users/', views.users_list, name='users'),

]
