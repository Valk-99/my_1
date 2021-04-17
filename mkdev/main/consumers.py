# Встроенные импорты.
import json

# Импорты сторонних библиотек.
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

# Импорты Django.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

# Локальные импорты.
from main.models import Product


class LiveScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       self.room_name = self.scope['url_route']['kwargs']['product_id']
       self.room_group_name = f'Product_{self.room_name}'

       if self.scope['user'] == AnonymousUser():
           raise DenyConnection("Такого пользователя не существует")

       await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
       )

       # If invalid game id then deny the connection.
       try:
            self.game = Product.objects.get(pk=self.room_name)
       except ObjectDoesNotExist:
            raise DenyConnection("Неверный ID игры")

       await self.accept()

    async def receive(self, text_data):
        in_stock = json.loads(text_data).get('in_stock')
        message = in_stock['message']

        # Send message to room group
        await self.channel_layer.group_send(
            [self.room_group_name, message]
        )

    async def websocket_disconnect(self, message):
        # Покинуть комнату группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )