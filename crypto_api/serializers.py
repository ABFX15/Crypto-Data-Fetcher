from rest_framework import serializers
from .models import CryptoPrice, CryptoMetaData, TrendingCrypto

class CryptoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPrice
        fields = ['id', 'crypto_id', 'date', 'price_usd', 'market_cap_usd', 'volume_24h_usd']

class CryptoMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoMetaData
        fields = ['id', 'crypto_id', 'name', 'symbol', 'description', 'market_cap_rank']

class TrendingCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingCrypto
        fields = ['id', 'crypto_id', 'name', 'symbol', 'market_cap_rank', 'score'] 