# Generated by Django 4.0 on 2023-07-17 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inboxes', '0003_messagenotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagenotification',
            name='receiver_inbx',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messagenotification', to='inboxes.inbox'),
        ),
    ]