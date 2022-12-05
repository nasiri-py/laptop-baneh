from products.models import Product, Color


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def __iter__(self):
        color_ids = self.cart.keys()
        colors = Color.objects.filter(id__in=color_ids)

        for color in colors:
            self.cart[str(color.id)]['color'] = color

        for item in self.cart.values():
            if item['color'].product.has_discount:
                price = item['color'].product.discount
            else:
                price = item['color'].product.price
            item['total_price'] = price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, color, quantity=1):
        color_id = str(color.id)
        if color_id not in self.cart:
            self.cart[color_id] = {
                'quantity': 0,
            }
        self.cart[color_id]['quantity'] += quantity
        self.save()

    def increase(self, color):
        color_id = str(color.id)
        self.cart[color_id]['quantity'] += 1
        if self.cart[color_id]['quantity'] >= color.number:
            self.cart[color_id]['quantity'] = color.number
        self.save()

    def decrease(self, color):
        color_id = str(color.id)
        self.cart[color_id]['quantity'] -= 1
        if self.cart[color_id]['quantity'] == 0:
            self.remove(color)
        self.save()

    def remove(self, color):
        color_id = str(color.id)
        if color_id in self.cart:
            del self.cart[color_id]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(item['quantity'] * item['color'].product.discount if item['color'].product.has_discount
                   else item['quantity'] * item['color'].product.price for item in self.cart.values())

    def total_discount(self):
        return sum(item['quantity'] * item['color'].product.price for item in self.cart.values()) - \
               self.get_total_price()

    def total_discount_percent(self):
        return int(((sum(item['quantity'] * item['color'].product.price for item in self.cart.values()) -
                     self.get_total_price()) * 100) / self.get_total_price())
