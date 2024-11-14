from rest_framework import viewsets

from .models import CryptoPrice
from .serializers import CryptoPriceSerializer


class CryptoPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CryptoPrice.objects.all().order_by('-timestamp')
    serializer_class = CryptoPriceSerializer
    ordering_fields = ('-timestamp',)


from django.views.generic import TemplateView


class WebSocketTestView(TemplateView):
    template_name = 'stream/test.html'
