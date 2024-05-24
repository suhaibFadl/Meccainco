# Generated by Django 4.0 on 2023-05-22 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_storeprofile_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storebranch',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='profiles.storeprofile'),
        ),
    ]