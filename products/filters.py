import django_filters
from django import forms
from .models import Brand, Category, CPUSeries, GPUMaker


class ProductFilter(django_filters.FilterSet):
    CHOICE_PRICE = (
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
    )

    CHOICE_CREATE = (
        ('قدیمی ترین', 'قدیمی ترین'),
        ('جدید ترین', 'جدید ترین')
    )

    CHOICE_FAVOURITE = (
        ('کم محبوب', 'کم محبوب'),
        ('محبوب ترین', 'محبوب ترین')
    )

    CHOICE_SELL = (
        ('کم فروش', 'کم فروش'),
        ('پرفروش ترین', 'پرفروش ترین')
    )

    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),
                                                     widget=forms.CheckboxSelectMultiple)
    grade = django_filters.AllValuesMultipleFilter(field_name='grade',
                                                   widget=forms.CheckboxSelectMultiple)
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple)
    screen_size = django_filters.AllValuesMultipleFilter(field_name='specs__screen_size',
                                                         widget=forms.CheckboxSelectMultiple)
    cpu_series = django_filters.ModelMultipleChoiceFilter(queryset=CPUSeries.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple)
    gpu_maker = django_filters.ModelMultipleChoiceFilter(queryset=GPUMaker.objects.all(),
                                                         widget=forms.CheckboxSelectMultiple)
    gpu_memory = django_filters.AllValuesMultipleFilter(field_name='specs__gpu_memory',
                                                        widget=forms.CheckboxSelectMultiple)
    ram_capacity = django_filters.AllValuesMultipleFilter(field_name='specs__ram_capacity',
                                                          widget=forms.CheckboxSelectMultiple)
    ssd_capacity = django_filters.AllValuesMultipleFilter(field_name='specs__ssd_capacity',
                                                          widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=CHOICE_PRICE, method='price_filter')
    create = django_filters.ChoiceFilter(choices=CHOICE_CREATE, method='create_filter')
    favourite = django_filters.ChoiceFilter(choices=CHOICE_FAVOURITE, method='favourite_filter')
    discount = django_filters.BooleanFilter(field_name='has_discount')
    sell = django_filters.ChoiceFilter(choices=CHOICE_SELL, method='sell_filter')

    def price_filter(self, queryset, name, value):
        data = 'price' if value == 'ارزان ترین' else '-price'
        return queryset.order_by('-available', data)

    def create_filter(self, queryset, name, value):
        data = 'created' if value == 'قدیمی ترین' else '-created'
        return queryset.order_by('-available', data)

    def favourite_filter(self, queryset, name, value):
        data = 'ratings__average' if value == 'کم محبوب' else '-ratings__average'
        return queryset.order_by('-available', data)

    # def sell_filter(self, queryset, name, value):
    #     data = 'sell' if value == 'کم فروش' else '-sell'
    #     return queryset.order_by('-available', data)
