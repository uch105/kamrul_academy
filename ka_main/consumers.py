# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LiveStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("live_stream", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("live_stream", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "live_stream",
            {
                "type": "stream_message",
                "message": data['message']
            }
        )

    async def stream_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
