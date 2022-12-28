from django.contrib import admin
from .models import Order, OrderItem, Coupon, OrderAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['color']
    extra = 0


class OrderAddressInline(admin.StackedInline):
    model = OrderAddress


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'ref_id', 'user', 'paid']
    list_filter = ['paid']
    search_fields = ['user__phone_number', 'address__phone_number', 'ref_id']
    inlines = [OrderItemInline, OrderAddressInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'discount_limit', 'valid_from', 'valid_to']