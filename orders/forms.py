from django import forms
from django.forms.models import ModelChoiceField
from products.models import Color
from .models import OrderAddress, Pay


class AddToCartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        self.fields['color'] = ModelChoiceField(queryset=Color.objects.filter(product_id=product_id),
                                                widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1)


class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = OrderAddress
        exclude = ['order']


class CouponForm(forms.Form):
    code = forms.CharField()


class PayForm(forms.ModelForm):
    class Meta:
        model = Pay
        exclude = ['order']
