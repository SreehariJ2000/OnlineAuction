
    
from django.urls import path
from Auction_app import consumers

websocket_urlpatterns = [
    path("chat/", consumers.ChatConsumer.as_asgi()),
]