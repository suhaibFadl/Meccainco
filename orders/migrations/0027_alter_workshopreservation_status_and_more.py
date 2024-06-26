# Generated by Django 4.0 on 2023-07-28 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_alter_workshopbranch_location'),
        ('orders', '0026_workshopreservation_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopreservation',
            name='status',
            field=models.IntegerField(choices=[(1, 'Requested'), (2, 'Confirmed'), (3, 'Done'), (4, 'Workshop Canceled'), (5, 'Customer Canceled')], default=1),
        ),
        migrations.CreateModel(
            name='WorkshopReservationNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_seen', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(1, 'Requested'), (4, 'Canceled')], default=1)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_notifications', to='profiles.workshopprofile')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.workshopreservation')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerReservationNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(2, 'Confirmed'), (3, 'Done'), (4, 'Canceled')], default=2)),
                ('is_seen', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_notifications', to='profiles.customerprofile')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.workshopreservation')),
            ],
        ),
    ]
