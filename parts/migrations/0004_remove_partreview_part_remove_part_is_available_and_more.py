# Generated by Django 4.0 on 2023-05-08 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0003_part_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partreview',
            name='part',
        ),
        migrations.RemoveField(
            model_name='part',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='part',
            name='price',
        ),
        migrations.RemoveField(
            model_name='part',
            name='status',
        ),
        migrations.DeleteModel(
            name='PartImage',
        ),
        migrations.DeleteModel(
            name='PartReview',
        ),
        migrations.DeleteModel(
            name='PartStatus',
        ),
    ]
