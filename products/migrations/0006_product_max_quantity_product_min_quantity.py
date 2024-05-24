# Generated by Django 4.0 on 2023-09-21 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='max_quantity',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='product',
            name='min_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
