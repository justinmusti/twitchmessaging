from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from core.models import Conversation, Message


class ChatConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None
    user = None

    def connect(self):
        from pprint import pprint
        pprint(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        # Ensure the user is logged in
        if not self.user.is_authenticated:
            self.close()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        conversation_id = self.room_name
        user = self.user

        convo = Conversation.objects.get(pk=conversation_id)
        msg = Message.objects.create(
            conversation=convo,
            user=user,
            text=message
        )
        data = {
                'sender_id': msg.user.pk.__str__(),
                'sender_username': msg.user.username,
                'text': msg.text,
                'created_at': msg.created_at.__str__(),
            }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data,

            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
