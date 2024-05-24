import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Message, Inbox, Contact, MessageNotification

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        sender_id = self.scope['url_route']['kwargs']['sender_id']
        receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        if int(sender_id) > int(receiver_id):
            self.room_name = f'{sender_id}-{receiver_id}'
        else:
            self.room_name = f'{receiver_id}-{sender_id}'

        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']
        receiver = data['receiver']

        await self.save_message(sender, self.room_group_name, message, receiver)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, username, thread_name, message, receiver):
        sender_inbox = Inbox.objects.get(owner=username)
        receiver_inbox = Inbox.objects.get(owner=receiver)
        # if sender_inbox.mainInbx.filter(contactInbx=receiver_inbox) :
        #     print('here1')
        # if  receiver_inbox.contactInbx.filter(mainInbx=sender_inbox):
        #     print('here2')
        # if   sender_inbox.mainInbx.filter(contactInbx=receiver_inbox) \
        #     or receiver_inbox.contactInbx.filter(mainInbx=sender_inbox):
        #     print("HEllo")
        Contact.objects.get_or_create(
            name=receiver_inbox.owner, 
            contactInbx=receiver_inbox, 
            mainInbx=sender_inbox
            )
        Contact.objects.get_or_create(
            name=sender_inbox.owner, 
            contactInbx=sender_inbox, 
            mainInbx=receiver_inbox
            )
        Message.objects.create(
            sender=sender_inbox, receiver=receiver_inbox, message=message, thread_name=thread_name)
        message_obj = Message.objects.filter(
            sender=sender_inbox, receiver=receiver_inbox, message=message, thread_name=thread_name).latest('id')
        # chat_obj = Message.objects.create(
        #     sender=sender_inbox, reciever=receiver_inbox, message=message, thread_name=thread_name)
        # other_user_id = self.scope['url_route']['kwargs']['id']
        # get_user = User.objects.get(id=other_user_id)
        # if receiver == get_user.username:
        MessageNotification.objects.create(message=message_obj, receiver_inbx=receiver_inbox)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        receiver_id = self.scope['user'].id
        self.room_group_name = f'notify-{receiver_id}'
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

    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        inbx_type = data['inbx_type']
        await self.send(text_data=json.dumps({
            'count': count,
            'inbx_type': inbx_type
        }))
        
        
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        print(connection_type)
        await self.change_online_status(username, connection_type)

    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']
        await self.send(text_data=json.dumps({
            'username':username,
            'online_status':online_status
        }))


    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def change_online_status(self, username, c_type):
        user = User.objects.get(username=username)
        userprofile = UserProfileModel.objects.get(user=user)
        if c_type == 'open':
            userprofile.online_status = True
            userprofile.save()
        else:
            userprofile.online_status = False
            userprofile.save()
