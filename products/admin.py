from django.contrib import admin
from .models import (
    Product,
    Color,
    Image,
    Category,
    Brand,
    Specification,
    Comment,
    IPAddress,
    CPUSeries,
    GPUMaker,
    Compare,
)


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


class ColorInline(admin.StackedInline):
    model = Color
    extra = 1


class SpecificationInline(admin.StackedInline):
    model = Specification


class ImageInline(admin.StackedInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover_tag', 'category_to_str', 'number', 'available', 'price', 'discount', 'j_created']
    change_list_template = 'products/product_admin.html'
    prepopulated_fields = {'slug': ('title',)}
    list_filter = (['brand', 'title', 'available'])
    search_fields = ('title', 'brand')
    ordering = ['-created', '-available']
    actions = [make_available, make_unavailable]
    inlines = [ColorInline, ImageInline, SpecificationInline]
    exclude = ("sell",)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_tag']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color_tag']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'body', 'is_reply', 'reply']
    raw_id_fields = ['reply']


class CompareAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'session_key']


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Compare, CompareAdmin)
admin.site.register(Specification)
admin.site.register(CPUSeries)
admin.site.register(GPUMaker)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(IPAddress)
