# Generated by Django 4.1.2 on 2023-01-02 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specification',
            name='etc',
            field=models.TextField(blank=True, null=True, verbose_name='سایر توضیحات'),
        ),
    ]
