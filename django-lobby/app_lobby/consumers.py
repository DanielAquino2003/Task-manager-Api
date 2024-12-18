import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.db.models import Q
from asgiref.sync import sync_to_async
import traceback
import time

class LobbyConsumer(AsyncWebsocketConsumer):

    # TODO: Implementar el método connect
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'lobby_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()