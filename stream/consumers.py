import asyncio
import json
import ssl
import websockets
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import CryptoPrice


class CryptoPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("crypto_prices", self.channel_name)
        await self.accept()

        # Start the background task to fetch prices
        await asyncio.create_task(self.fetch_prices())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("crypto_prices", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_price_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def save_price(self, symbol, price):
        CryptoPrice.objects.create(symbol=symbol, price=price)

    async def fetch_prices(self):
        # Using Binance's public WebSocket (as an example)
        uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"

        # Create an SSL context to ignore certificate verification
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        while True:
            try:
                async with websockets.connect(uri, ssl=ssl_context) as websocket:
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)

                        price_data = {
                            'symbol': 'BTCUSDT',
                            'price': float(data['p']),
                            'timestamp': data['T']
                        }

                        # Save to database
                        await self.save_price(price_data['symbol'], price_data['price'])

                        # Broadcast to all connected clients
                        await self.channel_layer.group_send(
                            "crypto_prices",
                            {
                                'type': 'send_price_update',
                                'data': price_data
                            }
                        )
            except Exception as e:
                print(f"WebSocket error: {e}")
                await asyncio.sleep(5)  # Wait before reconnecting