from django.urls import path
from app import consumers

websocket_urlpatterns = [
    path('ws/terminal/', consumers.TerminalConsumer.as_asgi()),
]
