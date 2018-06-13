from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/parking/$', consumers.ParkingConsumer),
    url(r'^ws/camera/$', consumers.CameraConsumer),
]
