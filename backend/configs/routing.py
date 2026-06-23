from apps.chat.consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('api/chat/<str:room>/', ChatConsumer.as_asgi()),
]