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


@register.inclusion_tag("products/partials/sort_input.html")
def sort_input(request, sort_val, content):
    return {
        "request": request,
        "sort_val": sort_val,
        "sort_q": f'sort={sort_val}',
        "content": content,
    }


@register.filter(name='is_in_list')
def is_in_list(value, given_list):
    return True if value in given_list else False
