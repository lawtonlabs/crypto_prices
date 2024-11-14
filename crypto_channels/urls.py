from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from stream import consumers, dctest
from stream.views import CryptoPriceViewSet, WebSocketTestView

router = DefaultRouter()
router.register(r'prices', CryptoPriceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('test/', WebSocketTestView.as_view(), name='websocket-test'),
    # re_path(r'ws/crypto/$', dctest.ChatConsumer.as_asgi()),
    re_path(r'ws/crypto/$', consumers.CryptoPriceConsumer.as_asgi()),
]
