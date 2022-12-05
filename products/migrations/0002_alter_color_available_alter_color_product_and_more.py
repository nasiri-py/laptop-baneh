# Generated by Django 4.1.2 on 2022-12-03 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='available',
            field=models.BooleanField(default=True, verbose_name='این رنگ از محصول موجود است'),
        ),
        migrations.AlterField(
            model_name='color',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='products.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True, verbose_name='محصول موجود است'),
        ),
    ]