from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from products.models import Product, Color
from .forms import AddToCartForm
from django.contrib import messages


def cart_view(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@require_POST
def cart_add_view(request, product_id):
    cart = Cart(request)
    # color = get_object_or_404(Color, id=color_id)
    form = AddToCartForm(request.POST, product_id=product_id)

    if form.is_valid():
        cd = form.cleaned_data

        cart.add(
            color=cd['color'],
            quantity=cd['quantity'],
        )
    messages.success(request, 'محصول با موفقیت به سبد خرید اضافه شد', 'success')
    return redirect('orders:cart')


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


# class OrderDetailView(LoginRequiredMixin, View):
#     form_class = CouponForm
#
#     def get(self, request, pk):
#         order = get_object_or_404(Order, pk=pk)
#         form = self.form_class()
#         if request.user == order.user:
#             return render(request, 'orders/order_detail.html', {'order': order, 'form': form})
#         return redirect('orders:cart')
