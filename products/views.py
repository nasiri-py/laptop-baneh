from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from .models import Product, Comment
from .forms import CommentForm
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.db.models import Min, Max, Q
from urllib.parse import urlencode
from django.contrib import messages
from orders.forms import AddToCartForm
from django.http import JsonResponse


def product_list_view(request):
    products = Product.objects.all().order_by('-available')
    mini = Product.objects.aggregate(m_price=Min('price'))
    min_price = int(mini['m_price'])
    maxi = Product.objects.aggregate(m_price=Max('price'))
    max_price = int(maxi['m_price'])

    filter_object = ProductFilter(request.GET, queryset=products)
    products = filter_object.qs

    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    data = request.GET.copy()
    if 'page' in data:
        del data['page']
    page_obj = paginator.get_page(page_number)

    context = {'filter': filter_object, 'page_obj': page_obj,
               'min_price': min_price, 'max_price': max_price, 'data': urlencode(data)}

    return render(request, 'products/product_list.html', context)


class ProductDetailView(generic.DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        self.colors = product.colors.filter(available=True)
        self.similar_products = Product.objects.filter(category__in=product.category.all()).exclude(id=product.id). \
                                    order_by('-available')[:10]
        product_id = {'product_id': product.id}
        self.order_form = AddToCartForm(**product_id)
        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['order_form'] = self.order_form
        context['similar_products'] = self.similar_products
        context['colors'] = self.colors
        return context


class CommentView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pk = self.kwargs.get('pk')

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.product = product
            new_form.save()
            messages.success(self.request, 'دیدگاه شما با موفقیت ثبت شد', 'success')
        return redirect('product:detail', product.slug)


class CommentReplyView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.product_pk = self.kwargs.get('product_pk')
        self.comment_pk = self.kwargs.get('comment_pk')

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.product_pk)
        comment = get_object_or_404(Comment, pk=self.comment_pk)
        form = CommentForm(request.POST or None)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.product = product
            new_form.reply = comment
            new_form.is_reply = True
            new_form.save()
            messages.success(self.request, 'دیدگاه شما با موفقیت ثبت شد', 'success')
        return redirect('product:detail', product.slug)


def search_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        product = request.GET.get('product')
        qs = Product.objects.filter(title__icontains=product)[:5]
        if len(qs) > 0 and len(product) > 0:
            data = []
            for pos in qs:
                item = {
                    'title': pos.title,
                    'slug': pos.slug,
                    'cover': str(pos.cover.url),
                }
                data.append(item)
            res = data
        else:
            res = 'محصول موردنظر یافت نشد ...'
        return JsonResponse({'data': res})
    return JsonResponse({})


class SearchList(generic.ListView):
    paginate_by = 20
    template_name = 'products/search_list.html'

    def get_queryset(self):
        search = self.request.GET.get('search')
        return Product.objects.filter(Q(title__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
