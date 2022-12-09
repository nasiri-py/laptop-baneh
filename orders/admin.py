from django.contrib import admin
from .models import Order, OrderItem, Coupon, OrderAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['color']


class OrderAddressInline(admin.StackedInline):
    model = OrderAddress


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'paid', 'updated']
    list_filter = ['paid']
    inlines = [OrderItemInline, OrderAddressInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'discount_limit', 'valid_from', 'valid_to']