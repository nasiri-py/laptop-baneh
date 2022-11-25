from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from colorfield.fields import ColorField
from django.utils.html import format_html
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=255)
    color = ColorField()

    def __str__(self):
        return self.title

    def color_tag(self):
        return format_html(f"<div style='height:20px; width:20px; border: 2px solid #bab5b5;"
                           f"border-radius: 50%; background-color:{self.color};'></div>")

    color_tag.short_description = "color"
    color_tag.allow_tags = True


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    cover = models.ImageField(upload_to='brands')

    def __str__(self):
        return self.name


class Product(models.Model):
    GRADE_CHOICES = (
        ('n', 'New'),
        ('o', 'Openbox'),
        ('s', 'Stoke')
    )

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    grade = models.CharField(choices=GRADE_CHOICES, max_length=1)
    category = models.ManyToManyField(Category, related_name="products")
    description = RichTextField(blank=True, null=True)
    color = models.ManyToManyField(Color)
    cover = models.ImageField(upload_to='products/cover/%Y/%m/%d')
    available = models.BooleanField(default=True)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    discount_percent = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name='hits')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.slug])

    def cover_tag(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.cover.url}'>")

    cover_tag.short_description = "cover"

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.all()])

    category_to_str.short_description = "category"

    def grade_choice(self):
        return [i[1] for i in self._meta.get_field('grade').choices if i[0] == self.grade][0]


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/%Y/%m/%d')

    def image_tag(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    image_tag.short_description = "image"


class Specification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='specs')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=2, decimal_places=1)
    size = models.CharField(max_length=255)
    # screen
    screen_size = models.DecimalField(max_digits=3, decimal_places=1)
    screen_type = models.CharField(max_length=255)
    screen_resolution = models.CharField(max_length=255)
    screen_matte = models.BooleanField(default=False)
    screen_touch = models.BooleanField(default=False)
    screen_description = models.TextField(blank=True, null=True)
    # cpu
    cpu_maker = models.CharField(max_length=255)
    cpu_series = models.CharField(max_length=255)
    cpu_model = models.CharField(max_length=255)
    cpu_description = models.TextField(blank=True, null=True)
    # gpu
    has_gpu = models.BooleanField(default=False)
    gpu_maker = models.CharField(max_length=255)
    gpu_model = models.CharField(max_length=255)
    gpu_memory = models.PositiveIntegerField(blank=True, null=True)
    gpu_description = models.TextField(blank=True, null=True)
    # ram
    ram_capacity = models.PositiveIntegerField()
    ram_type = models.CharField(max_length=255)
    ram_description = models.TextField(blank=True, null=True)
    # hard
    has_hdd = models.BooleanField(default=False)
    hdd_capacity = models.CharField(max_length=255, blank=True, null=True)
    has_ssd = models.BooleanField(default=False)
    ssd_capacity = models.CharField(max_length=255, blank=True, null=True)
    hard_description = models.TextField(blank=True, null=True)
    # ports and facilities
    optical_drive = models.BooleanField(default=False)
    webcam = models.CharField(max_length=255)
    touchpad_specs = models.CharField(max_length=255)
    keyboard_backlight = models.CharField(max_length=255)
    fingerprint = models.BooleanField(default=False)
    sd_card = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    bluetooth = models.CharField(max_length=255)
    ethernet = models.BooleanField(default=False)
    vga = models.BooleanField(default=False)
    hdmi = models.BooleanField(default=False)
    usb2_num = models.PositiveIntegerField(blank=True, null=True)
    usb3_num = models.PositiveIntegerField(blank=True, null=True)
    type_c = models.PositiveIntegerField(blank=True, null=True)
    thunderbolt = models.BooleanField(default=False)
    jack_3 = models.BooleanField(default=False)
    # other
    os = models.CharField(max_length=255)
    include_items = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='Your Comment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class ArticleHit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
