from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from products.models import Product, Color
from .forms import AddToCartForm
from django.contrib import messages
from .models import Order, OrderItem, Coupon, OrderAddress
from .forms import CouponForm, OrderAddressForm
from datetime import datetime
import pytz
from django.conf import settings
from django.http import HttpResponse
import requests
import json
from utils import send_sms
from accounts.models import User


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
    messages.success(request, 'محصول با موفقیت به سبد خرید اضافه شد', 'success')
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
    return redirect('orders:order-detail', order.id)


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    coupon_form = CouponForm()
    order_address_form = OrderAddressForm()
    if request.user == order.user:
        return render(request, 'orders/order_detail.html', {'order': order, 'oder_address_form': order_address_form,
                                                            'coupon_form': coupon_form})
    return redirect('orders:cart')


@login_required
def order_address_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
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
            return redirect('orders:order-pre-factor', order.id)
    return redirect('orders:cart')


@login_required
def order_pre_factor_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user == order.user:
        return render(request, 'orders/order_pre_factor.html', {'order': order})
    return redirect('orders:cart')


@login_required
def coupon_view(request, order_id):
    form = CouponForm(request.POST or None)
    now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
    if form.is_valid():
        try:
            coupon = Coupon.objects.get(code__exact=form.cleaned_data['code'],
                                        valid_from__lte=now, valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'این کد تخفیف وجود ندارد یا منقضی شده است', 'danger')
            return redirect('orders:order-factor', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.discount_limit = coupon.discount_limit
        order.save()
        messages.success(request, 'کد تخفیف با موفقیت اعمال شد', 'success')
    return redirect('orders:order-pre-factor', order_id)


@login_required
def order_pay_view(request, order_id):
    order = Order.objects.get(id=order_id)
    request.session['order_pay'] = {
        'order_id': order.id,
        'user_id': order.user.id,
    }
    req_data = {
        "merchant_id": settings.MERCHANT,
        "amount": order.get_total_cost() * 10,
        "callback_url": settings.CallbackURL,
        "description": settings.description,
        "metadata": {"mobile": request.user.phone_number, "email": settings.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=settings.ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(settings.ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        err_message = f"Error code: {e_code}, Error Message: {e_message}"
        return render(request, 'orders/pay_error.html', {'err_message': err_message})


@login_required
def order_verify_view(request):
    order_id = request.session['order_pay']['order_id']
    user_id = request.session['order_pay']['user_id']
    order = Order.objects.get(id=int(order_id), user=int(user_id))
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.get_total_cost() * 10,
            "authority": t_authority
        }
        req = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                admins = User.objects.get(is_staff=True)
                for admin in admins:
                    send_sms(admin.phone_number, f'کاربری با شماره موبایل {order.address.phone_number}'
                                                 f' و نام {order.address.full_name}'
                                                 f' سفارش با id {order.id} را پرداخت کرد'
                                                 f'\nشماره پیگیری: {str(req.json()["data"]["ref_id"])} ')
                send_sms(order.address.phone_number, f'با تشکر از اعتماد شما\nسفارش شما با موفقیت ثبت شد'
                                                     f'\nشماره پیگیری: {str(req.json()["data"]["ref_id"])} '
                                                     f'\n\nاستوک لپ تاپ استور')
                order.paid = True
                order.ref_id = str(req.json()["data"]["ref_id"])
                order.save()
                for item in order.items.all():
                    item.color.number -= item.quantity
                    if item.color.number == 0:
                        item.color.available = False
                    item.color.product.number -= item.quantity
                    if item.color.product.number == 0:
                        item.color.product.available = False
                    item.color.product.sell += item.quantity
                    item.color.save()
                    item.color.product.save()
                return render(request, 'orders/order_factor.html', {'order': order})
            elif t_status == 101:
                err_message = 'عملیات پرداخت قبلا با موفقیت انجام شده است: ' + str(req.json()['data']['message'])
                return render(request, 'orders/pay_error.html', {'err_message': err_message})
            else:
                err_message = 'Transaction failed.\nStatus: ' + str(req.json()['data']['message'])
                return render(request, 'orders/pay_error.html', {'err_message': err_message})
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            err_message = f"Error code: {e_code}, Error Message: {e_message}"
            return render(request, 'orders/pay_error.html', {'err_message': err_message})
    else:
        err_message = 'تراکنش ناموفق بوده یا توسط کاربر لغو شده است'
        return render(request, 'orders/pay_error.html', {'err_message': err_message})
