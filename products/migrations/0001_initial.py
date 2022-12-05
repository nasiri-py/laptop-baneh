# Generated by Django 4.1.2 on 2022-12-03 21:32

import ckeditor.fields
import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleHit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='مدل')),
                ('cover', models.ImageField(upload_to='brands', verbose_name='عکس کاور')),
            ],
            options={
                'verbose_name': 'یرند',
                'verbose_name_plural': 'برند ها',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'کاربری',
                'verbose_name_plural': 'کاربری ها',
            },
        ),
        migrations.CreateModel(
            name='CPUSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(max_length=255, verbose_name='سری پردازنده')),
            ],
            options={
                'verbose_name': 'سری پردازنده',
                'verbose_name_plural': 'سری های پردازنده',
            },
        ),
        migrations.CreateModel(
            name='GPUMaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maker', models.CharField(max_length=255, verbose_name='سازنده گرافیک')),
            ],
            options={
                'verbose_name': 'سازنده گرافیک',
                'verbose_name_plural': 'سازندگان گرافیک',
            },
        ),
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس IP')),
            ],
            options={
                'verbose_name': 'آدرس IP',
                'verbose_name_plural': 'آدرس های IP',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True, verbose_name='آدرس')),
                ('grade', models.CharField(choices=[('n', 'آکبند'), ('o', 'اپن باکس'), ('s', 'استوک')], max_length=1, verbose_name='گرید')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات')),
                ('cover', models.ImageField(upload_to='products/cover/%Y/%m/%d', verbose_name='عکس کاور')),
                ('available', models.BooleanField(default=True, verbose_name='موجود است')),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='تعداد موجودی')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('has_discount', models.BooleanField(default=False, verbose_name='تخفیف دارد')),
                ('discount', models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت تخفیف')),
                ('discount_percent', models.PositiveIntegerField(blank=True, null=True, verbose_name='درصد تخفیف')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='زمان ایجاد')),
                ('sell', models.IntegerField(default=0)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.brand', verbose_name='برند')),
                ('category', models.ManyToManyField(related_name='products', to='products.category', verbose_name='کاربری')),
                ('hits', models.ManyToManyField(blank=True, related_name='hits', through='products.ArticleHit', to='products.ipaddress')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام مدل')),
                ('weight', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='وزن')),
                ('size', models.CharField(max_length=255, verbose_name='ابعاد')),
                ('screen_size', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='ابعاد صفحه نمایش')),
                ('screen_type', models.CharField(max_length=255, verbose_name='نوع صفحه نمایش')),
                ('screen_resolution', models.CharField(max_length=255, verbose_name='رزولوشن')),
                ('screen_matte', models.BooleanField(default=False, verbose_name='صفحه نمایش مات')),
                ('screen_touch', models.BooleanField(default=False, verbose_name='صفحه نمایش لمسی')),
                ('screen_description', models.TextField(blank=True, null=True, verbose_name='توضیحات صفحه نمایش')),
                ('cpu_maker', models.CharField(max_length=255, verbose_name='سازنده پردازنده')),
                ('cpu_model', models.CharField(max_length=255, verbose_name='مدل پردازنده')),
                ('cpu_description', models.TextField(blank=True, null=True, verbose_name='توضیحات پردازنده')),
                ('has_gpu', models.BooleanField(default=False, verbose_name='گرافیک خارچی دارد')),
                ('gpu_model', models.CharField(max_length=255, verbose_name='مدل گرافیک')),
                ('gpu_memory', models.PositiveIntegerField(blank=True, null=True, verbose_name='حافظه گرافیک')),
                ('gpu_description', models.TextField(blank=True, null=True, verbose_name='توضیحات گرافیک')),
                ('ram_capacity', models.PositiveIntegerField(verbose_name='حافظه رم')),
                ('ram_type', models.CharField(max_length=255, verbose_name='نوع رم')),
                ('ram_description', models.TextField(blank=True, null=True, verbose_name='توضیحات رم')),
                ('has_hdd', models.BooleanField(default=False, verbose_name='هارد HDD دارد')),
                ('hdd_capacity', models.CharField(blank=True, max_length=255, null=True, verbose_name='حافظه HDD')),
                ('has_ssd', models.BooleanField(default=False, verbose_name='هارد SSD دارد')),
                ('ssd_capacity', models.CharField(blank=True, max_length=255, null=True, verbose_name='حافظه SSD')),
                ('hard_description', models.TextField(blank=True, null=True, verbose_name='توضیحات هارد')),
                ('optical_drive', models.BooleanField(default=False, verbose_name='درایو نوری دارد')),
                ('webcam', models.CharField(max_length=255, verbose_name='وبکم')),
                ('touchpad_specs', models.CharField(max_length=255, verbose_name='توضیحات تاچ پد')),
                ('keyboard_backlight', models.CharField(max_length=255, verbose_name='نور پس زمینه کیبورد')),
                ('fingerprint', models.BooleanField(default=False, verbose_name='سنسور اثرانگشت دارد')),
                ('sd_card', models.BooleanField(default=False, verbose_name='کارت خوان دارد')),
                ('wifi', models.BooleanField(default=False, verbose_name='وای فای دارد')),
                ('bluetooth', models.CharField(max_length=255, verbose_name='بلوتوث')),
                ('ethernet', models.BooleanField(default=False, verbose_name='درگاه شبکه دارد')),
                ('vga', models.BooleanField(default=False, verbose_name='درگاه VGA دارد')),
                ('hdmi', models.BooleanField(default=False, verbose_name='درگاه HDMI دارد')),
                ('usb2_num', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد درگاه USB2')),
                ('usb3_num', models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد درگاه USB3')),
                ('type_c', models.PositiveIntegerField(blank=True, null=True, verbose_name='نعداد درگاه Type C')),
                ('thunderbolt', models.BooleanField(default=False, verbose_name='درگاه Thunderbolt دارد')),
                ('jack_3', models.BooleanField(default=False, verbose_name='درگاه جک 3.5 دارد')),
                ('os', models.CharField(max_length=255, verbose_name='سیستم عامل')),
                ('include_items', models.CharField(max_length=255, verbose_name='اقلام همراه')),
                ('battery', models.CharField(max_length=255, verbose_name='باتری')),
                ('cpu_series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpu_series', to='products.cpuseries', verbose_name='سری پردازنده')),
                ('gpu_maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gpu_makers', to='products.gpumaker', verbose_name='سازنده گرافیک')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='specs', to='products.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'مشخصات',
                'verbose_name_plural': 'مشخصات',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/images/%Y/%m/%d', verbose_name='عکس')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'عکس',
                'verbose_name_plural': 'عکس ها',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='دیدگاه شما')),
                ('is_reply', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.product')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, verbose_name='رنگ')),
                ('available', models.BooleanField(default=True, verbose_name='این رنگ موجود است')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color', to='products.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'رنگ',
                'verbose_name_plural': 'رنگ ها',
            },
        ),
        migrations.AddField(
            model_name='articlehit',
            name='ip_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ipaddress'),
        ),
        migrations.AddField(
            model_name='articlehit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
