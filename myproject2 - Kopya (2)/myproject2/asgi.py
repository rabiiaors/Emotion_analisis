import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Emotion_detection import routing  # routing'in doğru şekilde import edildiğinden emin olun

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject2.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
