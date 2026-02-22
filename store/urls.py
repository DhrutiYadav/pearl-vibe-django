from django.urls import path
from . import views, views_extra

app_name = 'store'

urlpatterns = [
    path('', views.store, name='home'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),

    path('category/<int:category_id>/', views.subcategories, name='subcategory'),
    path('subcategory/<int:subcategory_id>/', views.products_by_subcategory, name='products_by_subcategory'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    path('about/', views_extra.about, name='about'),
    path('contact/', views_extra.contact, name='contact'),
    path('feedback/', views_extra.feedback, name='feedback'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),

    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),

]
