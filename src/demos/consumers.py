import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.channel_layer.group_add("chat", self.channel_name)
		await self.accept()

	async def disconnect(self, code):
		await self.channel_layer.group_discard("chat", self.channel_name)

	async def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		username = self.scope["user"].username

		await self.channel_layer.group_send(
			"chat",
			{
				'type': 'chat_message',
				'message': message,
				'username': username
			}
		)

	async def chat_message(self, event):
		message = event['message']
		username = event['username']

		await self.send(text_data=json.dumps({
			'message': message,
			'username': username
		}))
