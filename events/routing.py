from django.urls import re_path
from .consumers import RegisteredStudentConsumer

websocket_urlpatterns = [
    re_path(r"ws/event/(?P<slug>[\w-]+)/$", RegisteredStudentConsumer.as_asgi()),
]