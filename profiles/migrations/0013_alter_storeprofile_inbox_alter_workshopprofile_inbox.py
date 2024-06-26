# Generated by Django 4.0 on 2023-07-22 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inboxes', '0005_alter_messagenotification_receiver_inbx'),
        ('profiles', '0012_workshopprofile_workshopreview_workshopimage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeprofile',
            name='inbox',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inboxes.inbox'),
        ),
        migrations.AlterField(
            model_name='workshopprofile',
            name='inbox',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inboxes.inbox'),
        ),
    ]
