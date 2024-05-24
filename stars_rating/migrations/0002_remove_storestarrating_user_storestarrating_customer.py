# Generated by Django 4.0 on 2023-07-10 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_storeprofile_logo'),
        ('stars_rating', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storestarrating',
            name='user',
        ),
        migrations.AddField(
            model_name='storestarrating',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.customerprofile'),
        ),
    ]