from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Color
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='users', verbose_name='کاربر')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان سفارش')
    discount = models.IntegerField(blank=True, null=True, default=None, verbose_name='درصد تخفیف')
    discount_limit = models.IntegerField(blank=True, null=True, default=None, verbose_name='حداکثر مقدار تخفیف')

    class Meta:
        ordering = ('paid', '-updated')
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'{self.user} - {self.paid}'

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount is not None:
            total_discount = total - (self.discount * total) / 100
            if self.discount_limit is not None:
                if total - total_discount >= self.discount_limit:
                    total_discount = total - self.discount_limit
            return total_discount
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name='رنگ')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.IntegerField(default=1, verbose_name='تعداد')

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=50, verbose_name='کد تخفیف')
    valid_from = models.DateTimeField(verbose_name='زمان شروع')
    valid_to = models.DateTimeField(verbose_name='زمان پایان')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='درصد تخیف')
    discount_limit = models.IntegerField(blank=True, null=True, verbose_name='حداکثر مقدار تخفیف')
    active = models.BooleanField(default=False, verbose_name='فعال است')

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیفات'

    def __str__(self):
        return self.code


class OrderAddress(models.Model):
    # receiver
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    # address
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='address')
    state = models.CharField(max_length=255, verbose_name='استان')
    city = models.CharField(max_length=255, verbose_name='شهر')
    address = models.CharField(max_length=512, verbose_name='نشانی پستی')
    tag = models.IntegerField(verbose_name='پلاک')
    unit = models.IntegerField(blank=True, null=True, verbose_name='واحد')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'
