from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add_view, name='cart-add'),
    path('cart/remove/<int:color_id>/', views.cart_remove_view, name='cart-remove'),
    path('cart/increase/<int:color_id>/', views.cart_increase_view, name='cart-increase'),
    path('cart/decrease/<int:color_id>/', views.cart_decrease_view, name='cart-decrease'),
    path('cart/clear/', views.cart_clear_view, name='cart-clear'),
    path('create/', views.order_create_view, name='order-create'),
    path('detail/', views.order_detail_view, name='order-detail'),
    path('address/', views.order_address_view, name='order-address'),
    path('factor/', views.order_pre_factor_view, name='order-pre-factor'),
    path('coupon/<int:order_id>/', views.coupon_view, name='coupon'),
    path('pay/', views.OrderPayView.as_view(), name='order-pay'),
]
