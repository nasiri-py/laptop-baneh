from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from .models import Product, Comment
from .forms import CommentForm


class ProductListView(generic.ListView):
    paginate_by = 1
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.all().order_by('-available', '-created')
        return products


class ProductDetailView(generic.DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    form_class = CommentForm

    def get_object(self, queryset=None):
        global comment_form
        comment_form = CommentForm()
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = comment_form
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
        return redirect('product:detail', product.slug)
