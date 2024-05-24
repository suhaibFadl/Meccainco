import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NewBusinessNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        receiver_id = self.scope['user'].id
        self.room_group_name = f'order-notify-{receiver_id}'
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

    async def send_order_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        receiver_type = data['receiver_type']
        await self.send(text_data=json.dumps({
            'count': count,
            'receiver_type': receiver_type
        }))


