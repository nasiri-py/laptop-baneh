# Generated by Django 4.1.2 on 2022-11-30 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_specification_cpu_series_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_discount',
            field=models.BooleanField(default=False),
        ),
    ]
