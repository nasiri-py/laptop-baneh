from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.utils.html import format_html
from ckeditor.fields import RichTextField


class Category(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children')
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


class Image(models.Model):
    image = models.ImageField(upload_to='products/images/%Y/%m/%d')

    def image_tag(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.image.url}'>")

    image_tag.short_description = "image"


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    cover = models.ImageField(upload_to='brands/%Y/%m/%d')

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
    images = models.ManyToManyField(Image)
    available = models.BooleanField(default=True)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)

    def cover_tag(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.cover.url}'>")

    cover_tag.short_description = "cover"

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.all()])

    category_to_str.short_description = "category"


class Specification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='specs')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=1, decimal_places=1)
    size = models.CharField(max_length=255)
    # cpu
    cpu_maker = models.CharField(max_length=255)
    cpu_model = models.CharField(max_length=255)
    cpu_cache = models.PositiveIntegerField(null=True)
    cpu_description = models.TextField(blank=True, null=True)
    # gpu
    has_gpu = models.BooleanField(default=False)
    gpu_model = models.CharField(max_length=255, blank=True, null=True)
    gpu_memory = models.PositiveIntegerField(blank=True, null=True)
    gpu_description = models.TextField(blank=True, null=True)
    # ram
    ram_capacity = models.PositiveIntegerField()
    ram_type = models.CharField(max_length=255)
    ram_description = models.TextField(blank=True, null=True)
    # hard
    has_hdd = models.BooleanField(default=False)
    hdd_capacity = models.PositiveIntegerField(blank=True, null=True)
    has_ssd = models.BooleanField(default=False)
    ssd_capacity = models.PositiveIntegerField(blank=True, null=True)
    hard_description = models.TextField(blank=True, null=True)
    # screen
    screen_size = models.DecimalField(max_digits=1, decimal_places=1)
    screen_type = models.CharField(max_length=255)
    screen_resolution = models.CharField(max_length=255)
    screen_matte = models.BooleanField(default=False)
    screen_touch = models.BooleanField(default=False)
    screen_description = models.TextField(blank=True, null=True)
    # ports and facilities
    optical_drive = models.BooleanField(default=False)
    webcam = models.CharField(max_length=255)
    touchpad_specs = models.CharField(max_length=255)
    keyboard_backlight = models.CharField(max_length=255)
    card_reader = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    bluetooth = models.CharField(max_length=255)
    ethernet = models.BooleanField(default=False)
    vga = models.BooleanField(default=False)
    hdmi = models.BooleanField(default=False)
    usb2_num = models.PositiveIntegerField(blank=True, null=True)
    usb3_num = models.PositiveIntegerField(blank=True, null=True)
    type_c = models.BooleanField(default=False)
    thunderbolt = models.BooleanField(default=False)
    # other
    cat = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    include_items = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)

    def __str__(self):
        return self.name
