from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from . import consumers

websocket_urlpatterns = [
	re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
	{
		"websocket": AuthMiddlewareStack(
			URLRouter(websocket_urlpatterns)
		),
	}
)
