import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from demos.consumers import ChatConsumer  # Import your consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inpv.settings')

# Initialize Django ASGI application early
django_asgi_app = get_asgi_application()

# Define WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
]

# Configure the ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
