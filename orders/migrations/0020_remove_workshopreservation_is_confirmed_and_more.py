# Generated by Django 4.0 on 2023-07-25 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_workshopreservation_ordernotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopreservation',
            name='is_confirmed',
        ),
        migrations.AddField(
            model_name='workshopreservation',
            name='status',
            field=models.IntegerField(choices=[(1, 'Requested'), (2, 'confirmed'), (3, 'Done'), (4, 'Canceled')], default=1),
        ),
    ]
