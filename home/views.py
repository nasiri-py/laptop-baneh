from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta
from django.db.models import Count, Q, Max
from products.models import Product, Brand
from django.contrib.contenttypes.models import ContentType


class HomeView(View):
    def get(self, request):
        product_discount = Product.objects.filter(available=True, discount__isnull=False)
        product_newest = Product.objects.filter(discount__isnull=True).order_by('-created')[:10]

        last_ten_days = datetime.today() - timedelta(days=10)
        product_popular = Product.objects.filter(discount__isnull=True).annotate(
            count=Count('hits', filter=Q(articlehit__created__gt=last_ten_days))
        ).order_by('-count', '-created')[:10]

        content_type_id = ContentType.objects.get(app_label='products', model='brand').id
        brand_hot = Brand.objects.annotate(
            max=Max('ratings__average', filter=Q(ratings__content_type_id=content_type_id))
        ).order_by('-max', '-name')[:6]

        return render(request, 'home/home.html',
                      {'product_discount': product_discount, 'product_newest': product_newest,
                       'product_popular': product_popular, 'brand_hot': brand_hot})
