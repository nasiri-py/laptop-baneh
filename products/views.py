from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from .models import Product, Comment, Compare
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

    # get min and max price of products
    mini = Product.objects.aggregate(m_price=Min('price'))
    min_price = int(mini['m_price'])
    maxi = Product.objects.aggregate(m_price=Max('price'))
    max_price = int(maxi['m_price'])

    min_val_price = request.GET.get('pg')
    max_val_price = request.GET.get('pl')
    if min_val_price is None:
        min_val_price = min_price
    if max_val_price is None:
        max_val_price = max_price

    # apply filters
    filter_object = ProductFilter(request.GET, queryset=products)
    products = filter_object.qs

    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    data = request.GET.copy()
    if 'page' in data:
        del data['page']

    if ('pg' in data and 'pl' in data) and (data['pg'] == str(min_price) and data['pl'] == str(max_price)):
        del data['pg']
        del data['pl']

    if 'sort' in data:
        sort_val = data['sort']
    else:
        sort_val = 4

    data_na = data.copy()
    if 'im' in data_na:
        del data_na['im']

    page_obj = paginator.get_page(page_number)

    data_url = urlencode(list(data.lists()), doseq=True)
    data_na_url = urlencode(list(data_na.lists()), doseq=True)

    context = {'filter': filter_object, 'page_obj': page_obj, 'min_price': min_price, 'max_price': max_price,
               'min_val_price': min_val_price, 'max_val_price': max_val_price, 'data': data_url, 'data_na': data_na_url,
               'sort_val': sort_val}

    return render(request, 'products/product_list.html', context)


class ProductDetailView(generic.DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        self.colors = product.colors.filter(available=True)

        # offer products by category
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
            messages.success(self.request, 'دیدگاه شما ثبت شد')
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
            messages.success(self.request, 'دیدگاه شما ثبت شد')
        return redirect('product:detail', product.slug)


# live search
def search_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        product = request.GET.get('product')
        qs = Product.objects.filter(Q(code__icontains=product) | Q(title__icontains=product))[:5]
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


def compare_add_view(request, pk):
    if request.user.is_authenticated:
        com = Compare.objects.filter(user_id=request.user.id)
        qs = Compare.objects.filter(user_id=request.user.id, product_id=pk)
        if qs.exists():
            messages.warning(request, 'این محصول داخل صفحه مقایسه موجود است')
            return redirect('product:compare')
        elif len(com) >= 3:
            messages.error(request, 'حداکثر 3 محصول را میتوانید برای مقایسه انتخاب کنید')
            return redirect('product:compare')
        else:
            Compare.objects.create(user_id=request.user.id, product_id=pk, session_key=None)
    else:
        com = Compare.objects.filter(user_id=None, session_key=request.session.session_key)
        qs = Compare.objects.filter(user_id=None, product_id=pk, session_key=request.session.session_key)
        if qs.exists():
            messages.warning(request, 'این محصول داخل صفحه مقایسه موجود است')
            return redirect('product:compare')
        elif len(com) >= 3:
            messages.error(request, ' حداکثر 3 محصول را میتوانید برای مقایسه انتخاب کنید')
            return redirect('product:compare')
        else:
            if not request.session.session_key:
                request.session.create()
            Compare.objects.create(user_id=None, product_id=pk, session_key=request.session.session_key)
    return redirect('product:compare')


def compare_view(request):
    if request.user.is_authenticated:
        data = Compare.objects.filter(user_id=request.user.id)
        max_com = False
        if len(data) >= 3:
            max_com = True
    else:
        data = Compare.objects.filter(session_key__exact=request.session.session_key, user_id=None)
        max_com = False
        if len(data) >= 3:
            max_com = True
    return render(request, 'products/compare.html', {'data': data, 'max_com': max_com})


def compare_delete_view(request, pk):
    compare_obj = get_object_or_404(Compare, pk=pk)
    compare_obj.delete()
    return redirect('product:compare')


# live search
def compare_search_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        product = request.GET.get('com_product')
        qs = Product.objects.filter(Q(code__icontains=product) | Q(title__icontains=product))
        if len(qs) > 0 and len(product) > 0:
            data = []
            for pos in qs:
                item = {
                    'title': pos.title,
                    'id': pos.id,
                    'cover': str(pos.cover.url),
                }
                data.append(item)
            res = data
        else:
            res = 'محصول موردنظر یافت نشد ...'
        return JsonResponse({'data': res})
    return JsonResponse({})

