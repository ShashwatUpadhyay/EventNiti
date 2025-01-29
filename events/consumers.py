import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RegisteredStudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_slug = self.scope["url_route"]["kwargs"]["slug"]
        self.room_group_name = f"event_{self.event_slug}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(f"WebSocket connection established: {self.channel_name}")
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_update(self, event):
        students = event["students"]
        await self.send(text_data=json.dumps(students))
