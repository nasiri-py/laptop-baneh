from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from colorfield.fields import ColorField
from django.utils.html import format_html
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from extensions.utils import jalali_converter


class ColorManager(models.Manager):
    def is_available(self):
        return self.objects.filter(available=True)


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس IP')

    class Meta:
        verbose_name = 'آدرس IP'
        verbose_name_plural = 'آدرس های IP'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')

    class Meta:
        verbose_name = 'کاربری'
        verbose_name_plural = 'کاربری ها'

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name='مدل')
    cover = models.ImageField(upload_to='brands', verbose_name='عکس کاور')
    ratings = GenericRelation(Rating)

    class Meta:
        verbose_name = 'یرند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    GRADE_CHOICES = (
        ('n', 'آکبند'),
        ('o', 'اپن باکس'),
        ('s', 'استوک'),
    )

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name='برند')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    code = models.CharField(max_length=255, unique=True, verbose_name='کد محصول')
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True, verbose_name='آدرس')
    grade = models.CharField(choices=GRADE_CHOICES, max_length=1, verbose_name='گرید')
    category = models.ManyToManyField(Category, related_name="products", verbose_name='کاربری')
    description = RichTextField(blank=True, null=True, verbose_name='توضیحات')
    cover = models.ImageField(upload_to='products/cover/%Y/%m/%d', verbose_name='عکس کاور')
    available = models.BooleanField(default=True, verbose_name='محصول موجود است')
    number = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='تعداد موجودی')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    has_discount = models.BooleanField(default=False, verbose_name='تخفیف دارد')
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت تخفیف')
    discount_percent = models.PositiveIntegerField(blank=True, null=True, verbose_name='درصد تخفیف')
    created = models.DateTimeField(auto_now=True, verbose_name='زمان ایجاد')
    ratings = GenericRelation(Rating)
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name='hits')
    sell = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.slug])

    def cover_tag(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px; object-fit: contain;' src='{self.cover.url}'>")

    cover_tag.short_description = 'عکس کاور'

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.all()])

    category_to_str.short_description = 'کاربری'

    def grade_choice(self):
        return [i[1] for i in self._meta.get_field('grade').choices if i[0] == self.grade][0]

    def j_created(self):
        return jalali_converter(self.created)

    j_created.short_description = "زمان انتشار"


class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors', verbose_name='محصول')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    color = ColorField(verbose_name='رنگ')
    available = models.BooleanField(default=True, verbose_name='این رنگ از محصول موجود است')
    number = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='تعداد موجودی این رنگ')

    objects = ColorManager()

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    image = models.ImageField(upload_to='products/images/%Y/%m/%d', verbose_name='عکس')

    class Meta:
        verbose_name = 'عکس'
        verbose_name_plural = 'عکس ها'


class CPUSeries(models.Model):
    series = models.CharField(max_length=255, verbose_name='سری پردازنده')

    class Meta:
        verbose_name = 'سری پردازنده'
        verbose_name_plural = 'سری های پردازنده'

    def __str__(self):
        return self.series


class GPUMaker(models.Model):
    maker = models.CharField(max_length=255, verbose_name='سازنده گرافیک')

    class Meta:
        verbose_name = 'سازنده گرافیک'
        verbose_name_plural = 'سازندگان گرافیک'

    def __str__(self):
        return self.maker


class Specification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='specs', verbose_name='محصول')
    name = models.CharField(max_length=255, verbose_name='نام مدل')
    weight = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='وزن')
    size = models.CharField(max_length=255, verbose_name='ابعاد')
    # screen
    screen_size = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='ابعاد صفحه نمایش')
    screen_type = models.CharField(max_length=255, verbose_name='نوع صفحه نمایش')
    screen_resolution = models.CharField(max_length=255, verbose_name='رزولوشن')
    screen_matte = models.BooleanField(default=False, verbose_name='صفحه نمایش مات')
    screen_touch = models.BooleanField(default=False, verbose_name='صفحه نمایش لمسی')
    screen_description = models.TextField(blank=True, null=True, verbose_name='توضیحات صفحه نمایش')
    # cpu
    cpu_maker = models.CharField(max_length=255, verbose_name='سازنده پردازنده')
    cpu_series = models.ForeignKey(CPUSeries, on_delete=models.CASCADE, related_name='cpu_series',
                                   verbose_name='سری پردازنده')
    cpu_model = models.CharField(max_length=255, verbose_name='مدل پردازنده')
    cpu_description = models.TextField(blank=True, null=True, verbose_name='توضیحات پردازنده')
    # gpu
    has_gpu = models.BooleanField(default=False, verbose_name='گرافیک خارچی دارد')
    gpu_maker = models.ForeignKey(GPUMaker, on_delete=models.CASCADE, related_name='gpu_makers',
                                  verbose_name='سازنده گرافیک')
    gpu_model = models.CharField(max_length=255, verbose_name='مدل گرافیک')
    gpu_memory = models.PositiveIntegerField(blank=True, null=True, verbose_name='حافظه گرافیک')
    gpu_description = models.TextField(blank=True, null=True, verbose_name='توضیحات گرافیک')
    # ram
    ram_capacity = models.PositiveIntegerField(verbose_name='حافظه رم')
    ram_type = models.CharField(max_length=255, verbose_name='نوع رم')
    ram_description = models.TextField(blank=True, null=True, verbose_name='توضیحات رم')
    # hard
    has_hdd = models.BooleanField(default=False, verbose_name='هارد HDD دارد')
    hdd_capacity = models.CharField(max_length=255, blank=True, null=True, verbose_name='حافظه HDD')
    has_ssd = models.BooleanField(default=False, verbose_name='هارد SSD دارد')
    ssd_capacity = models.CharField(max_length=255, blank=True, null=True, verbose_name='حافظه SSD')
    hard_description = models.TextField(blank=True, null=True, verbose_name='توضیحات هارد')
    # ports and facilities
    optical_drive = models.BooleanField(default=False, verbose_name='درایو نوری دارد')
    webcam = models.CharField(max_length=255, verbose_name='وبکم')
    touchpad_specs = models.CharField(max_length=255, verbose_name='توضیحات تاچ پد')
    keyboard_backlight = models.CharField(max_length=255, verbose_name='نور پس زمینه کیبورد')
    fingerprint = models.BooleanField(default=False, verbose_name='سنسور اثرانگشت دارد')
    sd_card = models.BooleanField(default=False, verbose_name='کارت خوان دارد')
    wifi = models.BooleanField(default=False, verbose_name='وای فای دارد')
    bluetooth = models.CharField(max_length=255, verbose_name='بلوتوث')
    ethernet = models.BooleanField(default=False, verbose_name='درگاه شبکه دارد')
    vga = models.BooleanField(default=False, verbose_name='درگاه VGA دارد')
    hdmi = models.BooleanField(default=False, verbose_name='درگاه HDMI دارد')
    usb2_num = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد درگاه USB2')
    usb3_num = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد درگاه USB3')
    type_c = models.PositiveIntegerField(blank=True, null=True, verbose_name='نعداد درگاه Type C')
    thunderbolt = models.BooleanField(default=False, verbose_name='درگاه Thunderbolt دارد')
    jack_3 = models.BooleanField(default=False, verbose_name='درگاه جک 3.5 دارد')
    # other
    os = models.CharField(max_length=255, verbose_name='سیستم عامل')
    include_items = models.CharField(max_length=255, verbose_name='اقلام همراه')
    battery = models.CharField(max_length=255, verbose_name='باتری')

    class Meta:
        verbose_name = 'مشخصات'
        verbose_name_plural = 'مشخصات'

    def __str__(self):
        return self.name


class Compare(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    session_key = models.CharField(max_length=300, blank=True, null=True, verbose_name='سشن')

    class Meta:
        verbose_name = 'مقایسه'
        verbose_name_plural = 'مقایسه ها'

    def __str__(self):
        return self.product.title


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='دیدگاه شما')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'

    def __str__(self):
        return self.product.title


class ArticleHit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
