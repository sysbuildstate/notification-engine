import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        query_string = self.scope['query_string'].decode()
        token = self.extract_token(query_string)

        if not token:
            await self.close(code=4001)
            return

        try:
            UntypedToken(token)
            self.room_group_name = 'global_notifications'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except (InvalidToken, TokenError):
            await self.close(code=4001)

    async def disconnect(self, close_code: int) -> None:
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def send_notification(self, event: dict) -> None:
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'payload': event['payload']
        }))

    def extract_token(self, query_string: str) -> str:
        for param in query_string.split('&'):
            if param.startswith('token='):
                return param.split('=')[1]
        return ""