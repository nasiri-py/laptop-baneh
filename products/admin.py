from django.contrib import admin
from .models import Product, Color, Image, Category


def make_available(modeladmin, request, queryset):
    rows_updated = queryset.update(available=True)
    if rows_updated == 1:
        message_bit = "موجود شد."
    else:
        message_bit = "موجود شدند."
    modeladmin.message_user(request, "{} لپ تاپ {}".format(rows_updated, message_bit))


make_available.short_description = "موجود شدن لپ تاپ های انتخاب شده"


def make_unavailable(modeladmin, request, queryset):
    rows_updated = queryset.update(available=False)
    if rows_updated == 1:
        message_bit = "ناموجود شد."
    else:
        message_bit = "ناموجود شدند."
    modeladmin.message_user(request, "{} لپ تاپ {}".format(rows_updated, message_bit))


make_unavailable.short_description = "ناموجود شدن لپ تاپ های انتخاب شده"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover_tag', 'category_to_str', 'number', 'available', 'price', 'discount']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['images']
    list_filter = (['brand', 'title', 'available'])
    search_fields = ('title', 'brand')
    ordering = ['-created', '-available']
    actions = [make_available, make_unavailable]


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_tag']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['title', 'color_tag']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)