from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from products.models import Product, Color
from .forms import AddToCartForm
from django.contrib import messages
from .models import Order, OrderItem, Coupon
from .forms import PostalAddressForm, CouponForm
from datetime import datetime
import pytz


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
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    postal_form = PostalAddressForm()
    coupon_form = CouponForm()
    if request.user == order.user:
        return render(request, 'orders/order_detail.html', {'order': order, 'postal_form': postal_form,
                                                            'coupon_form': coupon_form})
    return redirect('orders:cart')


@login_required
def coupon_view(request, pk):
    form = CouponForm(request.POST or None)
    now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
    if form.is_valid():
        try:
            coupon = Coupon.objects.get(code__exact=form.cleaned_data['code'],
                                        valid_from__lte=now, valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'این کد تخفیف وجود ندارد یا منقضی شده است', 'danger')
            return redirect('orders:order-detail', pk)
        order = Order.objects.get(id=pk)
        order.discount = coupon.discount
        order.discount_limit = coupon.discount_limit
        order.save()
        messages.success(request, 'کد تخفیف با موفقیت اعمال شد', 'success')
    return redirect('orders:order-detail', pk)


@login_required
def order_create_view(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        product = Product.objects.get(id=item['color'].product.id)
        if product.has_discount:
            price = product.discount
        else:
            price = product.price
        OrderItem.objects.create(order=order, product=product, price=price, quantity=item['quantity'])
    cart.clear()
    return redirect('orders:order-detail', order.id)
