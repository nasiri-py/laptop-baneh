from django.contrib import admin
from .models import Order, OrderItem, Coupon, OrderAddress, Pay


class PayInline(admin.StackedInline):
    model = Pay
    readonly_fields = ['price', 'pay_ref']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['price']
    extra = 0


class OrderAddressInline(admin.StackedInline):
    model = OrderAddress


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'ref_id', 'get_total_cost', 'paid', 'status']
    readonly_fields = ['user', 'ref_id', 'get_total_cost']
    list_display = ['id', 'ref_id', 'address', 'paid', 'status', 'j_created', 'get_total_cost']
    list_filter = ['paid']
    search_fields = ['user__phone_number', 'address__phone_number', 'ref_id']
    inlines = [PayInline, OrderItemInline, OrderAddressInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'discount_limit', 'j_valid_from', 'j_valid_to']
