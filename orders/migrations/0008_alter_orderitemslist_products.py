# Generated by Django 4.0 on 2023-06-02 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0007_rename_orderitmeslist_orderitemslist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitemslist',
            name='products',
            field=models.ManyToManyField(null=True, to='products.Product'),
        ),
    ]