from django import template
from products.models import Product, Brand, Category, CPUSeries, GPUMaker

register = template.Library()


@register.inclusion_tag("products/partials/boolean_icon.html")
def boolean_icon(boolean):
    return {'boolean': boolean}


@register.inclusion_tag("partials/navbar_list.html")
def navbar_list():
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    cpu_series = CPUSeries.objects.all()
    gpu_makers = GPUMaker.objects.all()
    return {
        'products': products,
        'brands': brands,
        'categories': categories,
        'cpu_series': cpu_series,
        'gpu_makers': gpu_makers,
    }
