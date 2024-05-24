# Generated by Django 4.0 on 2023-07-26 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_alter_storeprofile_inbox_alter_workshopprofile_inbox'),
        ('orders', '0024_remove_workshopreservation_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopreservation',
            name='workshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.workshopprofile'),
        ),
    ]
