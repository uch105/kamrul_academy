from django.urls import path
from ka_main.consumers import StreamConsumer

websocket_urlpatterns = [
    path('ws/stream/', StreamConsumer.as_asgi()),
]