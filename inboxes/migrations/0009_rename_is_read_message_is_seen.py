# Generated by Django 4.0 on 2023-10-02 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inboxes', '0008_message_is_read'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='is_read',
            new_name='is_seen',
        ),
    ]