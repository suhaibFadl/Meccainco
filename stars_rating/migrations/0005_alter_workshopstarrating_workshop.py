# Generated by Django 4.0 on 2023-07-23 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_alter_storeprofile_inbox_alter_workshopprofile_inbox'),
        ('stars_rating', '0004_workshopstarrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopstarrating',
            name='workshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workshop_rating', to='profiles.workshopprofile'),
        ),
    ]
