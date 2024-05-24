# Generated by Django 4.0 on 2023-09-02 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_sales_counter'),
        ('stars_rating', '0006_remove_productstarrating_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstarrating',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_rating', to='products.product'),
        ),
    ]
