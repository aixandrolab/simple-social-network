import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.utils import timezone

from profiles.models import Chat, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        if not await self.is_user_in_chat():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'chat_message_event':
                await self.handle_chat_message(data)
            elif message_type == 'edit_message_event':
                await self.handle_edit_message(data)
            elif message_type == 'delete_message_event':
                await self.handle_delete_message(data)

        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': str(e)
            }))

    async def handle_chat_message(self, data):
        content = data.get('content', '').strip()
        if not content:
            return

        message = await self.create_message(content)

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message_event',
                'message_id': message.pk,
                'content': message.content,
                'sender_id': message.sender.id,
                'sender_name': message.sender.user.username,
                'sender_avatar_url': message.sender.avatar_url,
                'timestamp': message.timestamp.isoformat(),
            }
        )

    async def handle_edit_message(self, data):
        message_id = data.get('message_id')
        new_content = data.get('content', '').strip()

        if not new_content or not message_id:
            return

        updated_message = await self.edit_message_from_db(new_content, message_id)

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'edit_message_event',
                'message_id': updated_message.pk,
                'content': updated_message.content,
                'timestamp': updated_message.timestamp.isoformat(),
                'edited_at': updated_message.edited_at.isoformat(),
            }
        )

    async def handle_delete_message(self, data):
        message_id = data.get('message_id')
        if not message_id:
            return

        await self.delete_message_from_db(message_id)

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'delete_message_event',
                'message_id': message_id,
            }
        )

    async def chat_message_event(self, event):
        await self.send(text_data=json.dumps(event))

    async def edit_message_event(self, event):
        await self.send(text_data=json.dumps(event))

    async def delete_message_event(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def is_user_in_chat(self):
        return Chat.objects.filter(
            Q(user1=self.user.profile) | Q(user2=self.user.profile),
            id=self.chat_id
        ).exists()

    @database_sync_to_async
    def create_message(self, content):
        chat = Chat.objects.get(id=self.chat_id)
        return ChatMessage.objects.create(
            chat=chat,
            sender=self.user.profile,
            content=content,
        )

    @database_sync_to_async
    def edit_message_from_db(self, content, message_id):
        message = ChatMessage.objects.get(id=message_id, sender=self.user.profile)
        message.content = content
        message.edited_at = timezone.now()
        message.save()
        return message

    @database_sync_to_async
    def delete_message_from_db(self, message_id):
        try:
            message = ChatMessage.objects.get(id=message_id, sender=self.user.profile)
            message.delete()
        except Exception as e:
            print(e)
