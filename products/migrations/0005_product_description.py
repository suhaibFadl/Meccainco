# Generated by Django 4.0 on 2023-09-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_sales_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='Product', max_length=1000),
        ),
    ]
