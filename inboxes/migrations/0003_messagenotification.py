# Generated by Django 4.0 on 2023-07-13 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inboxes', '0002_alter_contact_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_seen', models.BooleanField(default=False)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inboxes.message')),
                ('receiver_inbx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inboxes.inbox')),
            ],
        ),
    ]
