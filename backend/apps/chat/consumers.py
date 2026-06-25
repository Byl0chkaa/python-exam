import datetime

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import F
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from apps.ads.models import CarAdModel
from apps.chat.models import ChatRoomModel, MessageModel

UserModel = get_user_model()


class ChatConsumer(GenericAsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.user_name = None

    async def connect(self):
        if not self.scope.get('user') or not getattr(self.scope['user'], 'is_authenticated', False):
            await self.close()
            return

        await self.accept()

        self.user_name = await self.get_profile_name()
        await self.channel_layer.group_add(
            f"user_{self.scope['user'].id}",
            self.channel_name
        )

        if 'room' in self.scope['url_route']['kwargs']:
            room_name = self.scope['url_route']['kwargs']['room']
            self.room, _ = await ChatRoomModel.objects.aget_or_create(name=room_name)

            await self.channel_layer.group_add(
                self.room.name,
                self.channel_name
            )

            messages = await self.get_last_five_messages()
            for name, text in messages:
                await self.send_json({
                    'message': text,
                    'user': name,
                    'request_id': str(datetime.datetime.now())
                })

            await self.channel_layer.group_send(
                self.room.name,
                {
                    'type': 'sender',
                    'message': f"{self.scope['user'].id}_{self.user_name} connected to chat"
                }
            )

    async def sender(self, data):
        await self.send_json(data)

    @action()
    async def send_message(self, data, request_id, action):
        if not self.room:
            return await self.send_json({"error": "You are not connected to a specific room."})

        text = data.get('text')
        if not text:
            return await self.send_json({"error": "Message text is empty."})

        await MessageModel.objects.acreate(room=self.room, user=self.scope['user'], text=text)

        await self.channel_layer.group_send(
            self.room.name,
            {
                'type': 'sender',
                'message': text,
                'user': f"{self.scope['user'].id}_{self.user_name}",
                'id': request_id
            }
        )

    @action()
    async def send_private_message(self, data, request_id, action):
        recipient_id = data.get('userId')
        ad_id = data.get('adId')
        text = data.get('text')

        if not recipient_id or not ad_id or not text:
            return await self.send_json({"error": "Missing userId, adId, or text"})

        current_user_id = self.scope['user'].id
        min_id = min(current_user_id, int(recipient_id))
        max_id = max(current_user_id, int(recipient_id))

        private_room_name = f"chat_ad_{ad_id}_users_{min_id}_{max_id}"
        private_room = await self.get_or_create_private_room(private_room_name, ad_id)

        if not private_room:
            return await self.send_json({"error": "Car Ad not found."})

        room_ready = await self.add_users_to_room(private_room, current_user_id, recipient_id)
        if not room_ready:
            return await self.send_json({"error": "Recipient user not found."})

        await MessageModel.objects.acreate(room=private_room, user=self.scope['user'], text=text)

        payload = {
            'type': 'sender',
            'message': text,
            'user': f"{current_user_id}_{self.user_name}",
            'room_name': private_room_name,
            'ad_id': ad_id,
            'id': request_id
        }

        await self.channel_layer.group_send(private_room_name, payload)
        await self.channel_layer.group_send(f"user_{recipient_id}", payload)

    @database_sync_to_async
    def get_profile_name(self):
        return getattr(self.scope['user'].profile, 'name', 'Unknown')

    @database_sync_to_async
    def get_last_five_messages(self):
        if not self.room:
            return []

        res = MessageModel.objects.filter(room=self.room).annotate(
            name=F('user__profile__name'),
            pk=F('user__pk')
        ).values('text', 'name', 'pk').order_by('-id')[:5]

        return list(reversed([(f"{msg['pk']}_{msg['name']}", msg['text']) for msg in res]))

    @database_sync_to_async
    def get_or_create_private_room(self, room_name, ad_id):
        try:
            ad = CarAdModel.objects.get(id=ad_id)
            room, _ = ChatRoomModel.objects.get_or_create(
                name=room_name,
                defaults={'is_private': True, 'ad': ad}
            )
            return room
        except CarAdModel.DoesNotExist:
            return None

    @database_sync_to_async
    def add_users_to_room(self, room, user1_id, user2_id):
        try:
            user1 = UserModel.objects.get(id=user1_id)
            user2 = UserModel.objects.get(id=user2_id)
            room.users.add(user1, user2)
            return True
        except UserModel.DoesNotExist:
            return False