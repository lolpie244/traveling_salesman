from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .urls import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        # handle http/https requests
        # "http": get_asgi_application(),
        # handle ws/wss requests
        "websocket": URLRouter(*websocket_urlpatterns),
    }
)

