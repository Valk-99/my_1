from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import LiveScoreConsumer

websockets = URLRouter([
    path(
        "ws/in_stock/<int:product_id>", LiveScoreConsumer,
        name="live-score",
    ),
])