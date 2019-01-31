from django.conf.urls import url
from .consumers import ChatConsumer


# `room_name` is conversation_id(core.models.Conversation.pk)
websocket_urlpatterns = [
    url(r'^ws/tmessage/(?P<room_name>[^/]+)/$', ChatConsumer),
]
