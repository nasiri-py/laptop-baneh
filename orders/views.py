from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from products.models import Product, Color
from .forms import AddToCartForm, CouponForm, OrderAddressForm, PayForm
from django.contrib import messages
from .models import Order, OrderItem, Coupon, OrderAddress, Pay
from datetime import datetime
import pytz
from utils import send_sms
from accounts.models import User
from django.core.mail import EmailMessage


def cart_view(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@require_POST
def cart_add_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST, product_id=product_id)

    if form.is_valid():
        cd = form.cleaned_data

        cart.add(
            color=cd['color'],
            quantity=cd['quantity'],
        )
    messages.success(request, 'محصول به سبد خرید اضافه شد')
    return redirect('product:detail', product.slug)


def cart_remove_view(request, color_id):
    cart = Cart(request)
    color = get_object_or_404(Color, id=color_id)
    cart.remove(color)
    return redirect('orders:cart')


def cart_increase_view(request, color_id):
    card = Cart(request)
    color = get_object_or_404(Color, id=color_id)
    card.increase(color)
    return redirect('orders:cart')


def cart_decrease_view(request, color_id):
    card = Cart(request)
    color = get_object_or_404(Color, id=color_id)
    card.decrease(color)
    return redirect('orders:cart')


def cart_clear_view(request):
    card = Cart(request)
    card.clear()
    return redirect('orders:cart')


@login_required
def order_create_view(request):
    cart = Cart(request)
    order_not_pay = Order.objects.filter(user=request.user, paid=False)
    if order_not_pay.exists():
        order_not_pay.delete()
    order = Order.objects.create(user=request.user)
    for item in cart:
        color = Color.objects.get(id=item['color'].id)
        product = Product.objects.get(id=item['color'].product.id)
        if product.has_discount:
            price = product.discount
        else:
            price = product.price
        OrderItem.objects.create(order=order, product=product, color=color, price=price, quantity=item['quantity'])
    cart.clear()
    return redirect('orders:order-detail')


@login_required
def order_detail_view(request):
    order = Order.objects.get(user=request.user, paid=False)
    order_address_form = OrderAddressForm()
    if request.user == order.user:
        return render(request, 'orders/order_detail.html', {'order': order, 'oder_address_form': order_address_form})
    return redirect('orders:cart')


@login_required
def order_address_view(request):
    order = Order.objects.get(user=request.user, paid=False)
    form = OrderAddressForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        try:
            OrderAddress.objects.get(order_id=order.id)
        except OrderAddress.DoesNotExist:
            OrderAddress.objects.create(
                order=order,
                state=cd['state'],
                city=cd['city'],
                address=cd['address'],
                tag=cd['tag'],
                unit=cd['unit'],
                postal_code=cd['postal_code'],
                description=cd['description'],
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                phone_number=cd['phone_number'],
            )
        if request.user == order.user:
            return redirect('orders:order-pre-factor')
    return render(request, 'orders/order_detail.html', {'form': form})


@login_required
def order_pre_factor_view(request):
    order = Order.objects.get(user=request.user, paid=False)
    form = PayForm()
    coupon_form = CouponForm()
    if request.user == order.user:
        return render(request, 'orders/order_pre_factor.html', {'order': order, 'form': form,
                                                                'coupon_form': coupon_form})
    return redirect('orders:cart')


@login_required
def coupon_view(request, order_id):
    form = CouponForm(request.POST)
    now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
    if form.is_valid():
        try:
            coupon = Coupon.objects.get(code__exact=form.cleaned_data['code'],
                                        valid_from__lte=now, valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'این کد تخفیف وجود ندارد یا منقضی شده است')
            return redirect('orders:order-pre-factor')
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.discount_limit = coupon.discount_limit
        order.save()
        messages.success(request, 'کد تخفیف به سفارش شما اعمال شد')
    return redirect('orders:order-pre-factor')


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request):
        form = PayForm()
        return render(request, 'orders/order_pay.html', {'form': form})

    def post(self, request):
        order = Order.objects.get(user=request.user, paid=False)
        form = PayForm(request.POST)
        if form.is_valid():
            try:
                Pay.objects.get(order_id=order.id)
            except Pay.DoesNotExist:
                Pay.objects.create(
                    order=order,
                    price=form.cleaned_data['price'],
                    pay_ref=form.cleaned_data['pay_ref'],
                )
                admins = User.objects.filter(is_staff=True)
                for admin in admins.all():
                    order_message = f'ظاهرا کاربری با شماره موبایل {order.address.phone_number}' \
                                    f' و نام {order.address.full_name}' \
                                    f' سفارش با id {order.id} را پرداخت کرد'
                    send_sms(admin.phone_number, order_message)
                    email = EmailMessage('ثبت سفارش', order_message, to=('email@email.com',))
                    email.send()
            if request.user == order.user:
                messages.success(request, 'سفارش شما ثبت شد و نتیجه آن از طریق پیامک اطلاع رسانی میشود')
                return redirect('home:home')
        return render(request, 'orders/order_pay.html', {'form': form})
