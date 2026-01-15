from django.urls import path
from . import views, views_extra

app_name = 'store'

urlpatterns = [
    path('', views.store, name='home'),
    path('category/<int:category_id>/', views.subcategories, name='subcategory'),
    path('subcategory/<int:subcategory_id>/', views.products_by_subcategory, name='products_by_subcategory'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('process_order/', views.process_order, name='process_order'),
    path('about/', views_extra.about, name='about'),
    path('contact/', views_extra.contact, name='contact'),
    path('feedback/', views_extra.feedback, name='feedback'),
]
