from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Product
from .forms import ProductForm
from django.utils.text import slugify


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 20
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(generic.DetailView):
    template_name = 'products/product_detail.html'

    def get_object(self, *args, **kwargs):
        slug = kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        return product
