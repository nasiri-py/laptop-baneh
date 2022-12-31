import django_filters
from django import forms
from .models import Product, Brand, Category, CPUSeries, GPUMaker
from datetime import datetime, timedelta
from django.db.models import Count, Q


class ProductFilter(django_filters.FilterSet):
    CHOICE_SORT = (
        ('1', 'گران ترین'),
        ('2', 'ارزان ترین'),
        ('3', 'قدیمی ترین'),
        ('4', 'جدید ترین'),
        ('5', 'کم محبوب'),
        ('6', 'محبوب ترین'),
        ('7', 'کم فروش'),
        ('8', 'پرفروش ترین'),
        ('0', 'کم بازدید'),
        ('9', 'پربازدید ترین')
    )

    pg = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    pl = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    br = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple,
                                                  field_name='brand')

    gr = django_filters.AllValuesMultipleFilter(field_name='grade',
                                                widget=forms.CheckboxSelectMultiple)

    ca = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple,
                                                  field_name='category')

    sz = django_filters.AllValuesMultipleFilter(field_name='specs__screen_size',
                                                widget=forms.CheckboxSelectMultiple)

    cs = django_filters.ModelMultipleChoiceFilter(queryset=CPUSeries.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple,
                                                  field_name='specs__cpu_series')

    gm = django_filters.ModelMultipleChoiceFilter(queryset=GPUMaker.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple,
                                                  field_name='specs__gpu_maker')

    gc = django_filters.AllValuesMultipleFilter(field_name='specs__gpu_memory',
                                                widget=forms.CheckboxSelectMultiple)

    rc = django_filters.AllValuesMultipleFilter(field_name='specs__ram_capacity',
                                                widget=forms.CheckboxSelectMultiple)

    sc = django_filters.AllValuesMultipleFilter(field_name='specs__ssd_capacity',
                                                widget=forms.CheckboxSelectMultiple)

    im = django_filters.AllValuesMultipleFilter(field_name='available')

    di = django_filters.AllValuesMultipleFilter(field_name='has_discount')

    sort = django_filters.ChoiceFilter(choices=CHOICE_SORT, method='sort_filter')

    def sort_filter(self, queryset, name, value):
        if value == '1':
            data = '-price'
        elif value == '2':
            data = 'price'
        elif value == '3':
            data = 'created'
        elif value == '4':
            data = '-created'
        elif value == '5':
            data = 'ratings__average'
        elif value == '6':
            data = '-ratings__average'
        elif value == '7':
            data = 'sell'
        elif value == '8':
            data = '-sell'
        elif value == '0':
            data = 'hits'
        else:
            last_ten_days = datetime.today() - timedelta(days=10)
            product_popular = Product.objects.annotate(
                count=Count('hits', filter=Q(articlehit__created__gt=last_ten_days)))
            return product_popular.order_by('-available', '-count')
        return queryset.order_by('-available', data)
