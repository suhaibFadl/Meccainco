# Generated by Django 4.0 on 2023-05-15 17:05

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('inboxes', '0001_initial'),
        ('profiles', '0003_remove_storebranch_parts_storeprofile_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='inbox',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='inboxes.inbox'),
        ),
        migrations.AddField(
            model_name='storeprofile',
            name='inbox',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='inboxes.inbox'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='phone_num',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default='+218920000000', max_length=128, region=None, unique=True),
        ),
    ]
