from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WorkshopReservation, Order,\
    WorkshopReservationNotification,\
    CustomerReservationNotification,\
    StoreOrderNotification,\
    CustomerOrderNotification
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=WorkshopReservation)
def send_notification(sender, instance, created, **kwargs):
    if  instance.get_status_display() == 'Requested' \
        or instance.get_status_display() == 'Confirmed' \
        or instance.get_status_display() == 'Customer Canceled':

        receiver_id = instance.workshop.workshop.owner.id
        receiver_type = 'workshop'
        WorkshopReservationNotification.objects.create(
            receiver = instance.workshop.workshop,
            reservation = instance
        )
        notify_count = instance.workshop.workshop\
            .count_unseen_reservations_notifications()
         
    elif instance.get_status_display() == 'Make an Appointment' \
        or instance.get_status_display() == 'Car In The Garage' \
        or instance.get_status_display() == 'Under The Maintenance' \
        or instance.get_status_display() == 'Fixed' \
        or instance.get_status_display() == 'Workshop Canceled':
        print('Make an Appoinment')
        receiver_id = instance.customer.user.id
        CustomerReservationNotification.objects.create(
            receiver = instance.customer,
            reservation = instance
        )
        receiver_type = 'customer'
        notify_count = instance.customer.count_unseen_reservations_notifications()

    channel_layer = get_channel_layer()
    if instance.get_status_display() == 'Requested':
        
        reservation_data = {
        'id': instance.id,
        'status': instance.get_status_display(),
        'customer': instance.customer.user.username,
        }
        async_to_sync(channel_layer.group_send)(
                f'append-reservation-{instance.workshop.workshop.id}', {
                    'type':'append_reservation',
                    'value':json.dumps(reservation_data)
                }
            )  
    notify_data = {
        'count': notify_count,
        'receiver_type': receiver_type
    }
    async_to_sync(channel_layer.group_send)(
        f'reservation-notify-{receiver_id}', {
            'type':'send_reservation_notification',
            'value':json.dumps(notify_data), 
        }
    )

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if (instance.get_status_display() == 'Waiting' \
        or instance.get_status_display() == 'Customer Canceled')\
        and instance.confirmed == True:

        receiver_id = instance.store.owner.id
        receiver_type = 'store'
        StoreOrderNotification.objects.create(
            receiver = instance.store,
            order = instance
        )
        notify_count = instance.store\
            .count_unseen_orders_notifications()
    elif instance.get_status_display() == 'In Progress' \
        or instance.get_status_display() == 'En Route' \
        or instance.get_status_display() == 'Delivered' \
        or instance.get_status_display() == 'Product Unavailable'\
        or instance.get_status_display() == 'Store Canceled':
        
        receiver_id = instance.customer.user.id
        CustomerOrderNotification.objects.create(
            receiver = instance.customer,
            order = instance
        )
        receiver_type = 'customer'
        notify_count = instance.customer.count_unseen_orders_notifications()
    else: return
    print("heeere", receiver_type, notify_count)
    channel_layer = get_channel_layer()
    
    notify_data = {
        'count': notify_count,
        'receiver_type': receiver_type
    }

    async_to_sync(channel_layer.group_send)(
        f'order-notify-{receiver_id}', {
            'type':'send_order_notification',
            'value':json.dumps(notify_data), 
        }
    )

    
