import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Product, Comment


class AddCommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        product_id = self.scope['url_route']['kwargs']['product_id']
        self.room_group_name = f'{product_id}_product_comments'
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

    async def add_comment(self, event):
        comment = json.loads(event.get('value'))
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print("heeeeeere", comment)
        await self.send(text_data=json.dumps({
            'comment': comment,
        }))
        