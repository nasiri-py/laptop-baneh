from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.cart_add_view, name='cart-add'),
    path('remove/<int:color_id>/', views.cart_remove_view, name='cart-remove'),
    path('increase/<int:color_id>/', views.cart_increase_view, name='cart-increase'),
    path('decrease/<int:color_id>/', views.cart_decrease_view, name='cart-decrease'),
    path('clear/', views.cart_clear_view, name='cart-clear'),
]
