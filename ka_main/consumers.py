import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'stream'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Broadcast the video data to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_message',
                    'bytes_data': bytes_data
                }
            )

    async def video_message(self, event):
        bytes_data = event['bytes_data']

        # Send video data to WebSocket
        await self.send(bytes_data=bytes_data)