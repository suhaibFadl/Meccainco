# Generated by Django 4.0 on 2023-08-29 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('profiles', '0017_meccanicoadmin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerprofile',
            options={'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='meccanicoadmin',
            options={'verbose_name_plural': 'Meccainco Admins'},
        ),
        migrations.AlterModelOptions(
            name='storebranch',
            options={'verbose_name_plural': 'Stores Branches'},
        ),
        migrations.AlterModelOptions(
            name='storeimage',
            options={'verbose_name_plural': 'Stores Images'},
        ),
        migrations.AlterModelOptions(
            name='storeprofile',
            options={'verbose_name_plural': 'Stores'},
        ),
        migrations.AlterModelOptions(
            name='storereview',
            options={'verbose_name_plural': 'Stores Reviews'},
        ),
        migrations.AlterModelOptions(
            name='workshopbranch',
            options={'verbose_name_plural': 'Workshops Branches'},
        ),
        migrations.AlterModelOptions(
            name='workshopimage',
            options={'verbose_name_plural': 'Workshops Images'},
        ),
        migrations.AlterModelOptions(
            name='workshopprofile',
            options={'verbose_name_plural': 'Workshops'},
        ),
        migrations.AlterModelOptions(
            name='workshopreview',
            options={'verbose_name_plural': 'Workshops Reviews'},
        ),
        migrations.AlterField(
            model_name='meccanicoadmin',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]