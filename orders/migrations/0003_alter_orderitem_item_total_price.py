# Generated by Django 4.0 on 2023-05-06 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem_item_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_total_price',
            field=models.IntegerField(),
        ),
    ]
