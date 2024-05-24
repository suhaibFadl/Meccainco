from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MessageNotification
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=MessageNotification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        receiver_id = 0
        if instance.receiver_inbx.type == 0:
            receiver_id = str(instance.receiver_inbx.meccanicoadmin.admin.id)
        if instance.receiver_inbx.type == 1:
            receiver_id = str(instance.receiver_inbx.customerprofile.user.id)
        elif instance.receiver_inbx.type == 2:
            receiver_id = str(instance.receiver_inbx.storeprofile.owner.id)
        elif instance.receiver_inbx.type == 3:
            receiver_id = str(instance.receiver_inbx.workshopprofile.owner.id)
        channel_layer = get_channel_layer()
        notification_count = MessageNotification.objects.filter(is_seen=False, receiver_inbx=instance.receiver_inbx).count()
        inbx_type = instance.receiver_inbx.type
        data = {
            'count':notification_count,
            'inbx_type' : inbx_type
        }

        async_to_sync(channel_layer.group_send)(
            f'notify-{receiver_id}', {
                'type':'send_notification',
                'value':json.dumps(data), 
            }
        )