from apps.chat.routing import websocket_urlpatterns as chat_routing
from channels.routing import URLRouter
from django.urls import path

websocket_urlpatterns = [
    path('api/chat/', URLRouter(chat_routing)),
]