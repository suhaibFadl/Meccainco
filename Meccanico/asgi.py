"""
ASGI config for Meccanico project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

from inboxes.consumers import PersonalChatConsumer, \
    NotificationConsumer
from orders.consumers import AppendOrderConsumer, \
    ReservationNotificationConsumer, AppendReservationConsumer,\
    OrderNotificationConsumer
from products.consumers import AddCommentConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Meccanico.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:receiver_id>-<str:sender_id>/', PersonalChatConsumer.as_asgi()),
            path('ws/<str:store_id>orders/', AppendOrderConsumer.as_asgi()),
            path('ws/<str:workshop_id>reservations/', AppendReservationConsumer.as_asgi()),
            path('ws/<str:product_id>product/', AddCommentConsumer.as_asgi()),
            path('ws/notify/', NotificationConsumer.as_asgi()),
            path('ws/reservation-notify/', ReservationNotificationConsumer.as_asgi()),
            path('ws/order-notify/', OrderNotificationConsumer.as_asgi()),
            # path('ws/<str:receiver_id>-<str:sender_id>/', PersonalChatConsumer.as_asgi()),
            # path('ws/online/', OnlineStatusConsumer.as_asgi()),
            # path('ws/notify/', NotificationConsumer.as_asgi())
        ])
    )
})