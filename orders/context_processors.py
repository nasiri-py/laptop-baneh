from .cart import Cart


# access to cart in all templates (like user)
def cart(request):
    return {'cart': Cart(request)}
