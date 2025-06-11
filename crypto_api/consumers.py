import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import CryptoPrice

class CryptoPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'crypto_prices',
            self.channel_name
        )
        await self.accept() 
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'crypto_prices',
            self.channel_name 
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'subscribe':
            await self.channel_layer.group_add(
                f'crypto_{data['crypto_id']}',
                self.channel_name 
            )
            
    async def send_price_update(self, event):
        await self.send(text_data=json.dumps(event['data']))