import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class AppendOrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        store_id = self.scope['url_route']['kwargs']['store_id']
        self.room_group_name = f'append-order-{store_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def append_order(self, event):
        order = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({
            'data':order
        }))


class AppendReservationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        workshop_id = self.scope['url_route']['kwargs']['workshop_id']
        self.room_group_name = f'append-reservation-{workshop_id}'
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def append_reservation(self, event):
        reservation = json.loads(event.get('value'))
        print('heeeeeeeeeeer, hello')
        await self.send(text_data=json.dumps({
            'reservation': reservation,
        }))


class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        receiver_id = self.scope['user'].id
        self.room_group_name = f'order-notify-{receiver_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name)
        await self.accept()
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_order_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        receiver_type = data['receiver_type']
        await self.send(text_data=json.dumps({
            'count': count,
            'receiver_type': receiver_type
        }))


class ReservationNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        receiver_id = self.scope['user'].id
        self.room_group_name = f'reservation-notify-{receiver_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_reservation_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        receiver_type = data['receiver_type']
        await self.send(text_data=json.dumps({
            'count': count,
            'receiver_type': receiver_type
        }))