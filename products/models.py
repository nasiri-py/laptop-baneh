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


class Product(models.Model):
    brand = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    category = models.ManyToManyField(Category, related_name="products")
    description = RichTextField(blank=True, null=True)
    specs = RichTextField()
    color = models.ManyToManyField(Color)
    cover = models.ImageField(upload_to='products/cover/%Y/%m/%d')
    images = models.ManyToManyField(Image)
    available = models.BooleanField(default=True)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField(null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)

    def cover_tag(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 5px;' src='{self.cover.url}'>")

    cover_tag.short_description = "cover"

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.all()])

    category_to_str.short_description = "category"
