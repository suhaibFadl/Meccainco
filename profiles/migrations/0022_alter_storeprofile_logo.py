# Generated by Django 4.0 on 2023-10-01 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0021_rename__1st_number_storebranch_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeprofile',
            name='logo',
            field=models.ImageField(default='default_store.png', unique=True, upload_to='stores_logos'),
        ),
    ]
