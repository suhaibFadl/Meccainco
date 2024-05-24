# Generated by Django 4.0 on 2023-09-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_workshopreservation_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopreservation',
            name='status',
            field=models.IntegerField(choices=[(1, 'Requested'), (2, 'Make an Appointment'), (3, 'Confimed'), (4, 'Car In The Garage'), (5, 'Under The Maintenance'), (6, 'Finish'), (7, 'Workshop Canceled'), (8, 'Customer Canceled'), (8, 'Expired')], default=1),
        ),
    ]