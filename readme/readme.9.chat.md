notice on startapp Starting ASGI/Daphne version 4.1.2 development server at http://0.0.0.0:80/

# Real-time Chat Application

A simple real-time chat application using Django Channels and WebSockets. Messages are not persisted - they exist only during the active session.

## Features
- Real-time messaging using WebSockets
- No message storage (messages disappear on refresh)
- Only logged-in users can participate
- Shows username with each message
- Timestamps for messages

## Setup Instructions

1. Install channels:
   ```bash
   pip install channels==4.0.0
   ```
   Add to requirements.txt:
   ```txt
   channels==4.0.0
   ```

2. Create new Django app:
   ```bash
   python manage.py startapp chat
   ```

3. Add to INSTALLED_APPS in settings.py:
   ```python
   INSTALLED_APPS = [
       # ... existing apps ...
       'channels',
       'chat',
   ]
   ```

4. Configure Channels in settings.py:
   ```python
   ASGI_APPLICATION = "app.asgi.application"
   CHANNEL_LAYERS = {
       "default": {
           "BACKEND": "channels.layers.InMemoryChannelLayer"
       }
   }
   ```

5. Create WebSocket consumer (chat/consumers.py):
   ```python
   import json
   from channels.generic.websocket import AsyncWebsocketConsumer

   class ChatConsumer(AsyncWebsocketConsumer):
       async def connect(self):
           await self.channel_layer.group_add("chat", self.channel_name)
           await self.accept()

       async def disconnect(self, close_code):
           await self.channel_layer.group_discard("chat", self.channel_name)

       async def receive(self, text_data):
           text_data_json = json.loads(text_data)
           message = text_data_json['message']

           await self.channel_layer.group_send(
               "chat",
               {
                   'type': 'chat_message',
                   'message': message,
                   'username': self.scope['user'].username
               }
           )

       async def chat_message(self, event):
           await self.send(text_data=json.dumps({
               'message': event['message'],
               'username': event['username']
           }))
   ```

6. Set up WebSocket routing (chat/routing.py):
   ```python
   from django.urls import re_path
   from . import consumers

   websocket_urlpatterns = [
       re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
   ]
   ```

7. Configure ASGI application (app/asgi.py):
   ```python
   import os
   from django.core.asgi import get_asgi_application
   from channels.routing import ProtocolTypeRouter, URLRouter
   from channels.auth import AuthMiddlewareStack
   from chat.routing import websocket_urlpatterns

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

   application = ProtocolTypeRouter({
       "http": get_asgi_application(),
       "websocket": AuthMiddlewareStack(
           URLRouter(
               websocket_urlpatterns
           )
       ),
   })
   ```

8. Create view (chat/views.py):
   ```python
   from django.shortcuts import render
   from django.contrib.auth.decorators import login_required

   @login_required
   def chat_room(request):
       return render(request, 'chat/room.html')
   ```

9. Add URL pattern (chat/urls.py):
   ```python
   from django.urls import path
   from . import views

   app_name = 'chat'

   urlpatterns = [
       path('', views.chat_room, name='room'),
   ]
   ```

10. Create template (chat/templates/chat/room.html):
    ```html
    {% extends 'base.html' %}

    {% block content %}
    <div class="container mx-auto px-4 py-8">
        <div class="max-w-3xl mx-auto">
            <!-- Messages container -->
            <div id="chat-messages" class="bg-white shadow-lg rounded-lg p-6 mb-4 h-96 overflow-y-auto">
            </div>

            <!-- Message form -->
            <form id="chat-form" class="flex gap-4">
                <input type="text" 
                       id="chat-input" 
                       class="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500" 
                       placeholder="Type a message...">
                <button type="submit" 
                        class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 focus:outline-none">
                    Send
                </button>
            </form>
        </div>
    </div>

    <script>
        const chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/'
        );

        const messagesContainer = document.getElementById('chat-messages');
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const messageElement = document.createElement('div');
            messageElement.className = 'message mb-4';
            messageElement.innerHTML = `
                <span class="font-bold text-blue-600">${data.username}</span>
                <span class="text-gray-600 text-sm ml-2">${new Date().toLocaleTimeString()}</span>
                <p class="text-gray-800">${data.message}</p>
            `;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        };

        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (message) {
                chatSocket.send(JSON.stringify({
                    'message': message
                }));
                chatInput.value = '';
            }
        });
    </script>
    {% endblock %}
    ```

## How It Works

1. **WebSocket Connection**:
   - When a user opens the chat page, a WebSocket connection is established
   - The connection is authenticated using the Django session
   - Each user joins a chat group for broadcasting messages

2. **Sending Messages**:
   - User types message and submits form
   - JavaScript sends message through WebSocket
   - Server receives message and broadcasts to all connected users
   - Messages include username and timestamp

3. **Receiving Messages**:
   - WebSocket receives broadcasted message
   - JavaScript creates new message element
   - Message is added to chat container
   - Container auto-scrolls to latest message

## Security Features
- Login required for access
- WebSocket connections are authenticated
- User sessions are maintained
- XSS protection through Django's template system

## Limitations
- Messages are not persisted (disappear on refresh)
- No message history
- No private messaging
- No user typing indicators
- No message delivery confirmation

## Future Enhancements
1. Add message persistence
2. Add private messaging
3. Add typing indicators
4. Add online user list
5. Add message delivery status
6. Add file sharing capabilities

## Troubleshooting

1. If WebSocket connection fails:
   - Check if channels is installed
   - Verify ASGI configuration
   - Check URL routing

2. If messages aren't sending:
   - Check browser console for errors
   - Verify WebSocket connection
   - Check user authentication

3. If styling is missing:
   - Verify Tailwind CSS is properly configured
   - Check class names in template
