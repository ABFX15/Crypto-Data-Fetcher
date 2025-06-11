from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from ..models import CryptoPrice, CryptoMetaData, TrendingCrypto
from ..serializers import CryptoPriceSerializer, CryptoMetaDataSerializer, TrendingCryptoSerializer
from .services import CryptoAPIService

class CryptoPriceViewSet(viewsets.ModelViewSet):
    queryset = CryptoPrice.objects.all()
    serializer_class = CryptoPriceSerializer
    
    @action(detail=False, methods=['get'])
    def latest_prices(self, request):
        # Get crypto IDs from the database
        crypto_ids = CryptoMetaData.objects.values_list('crypto_id', flat=True)
        
        # Fetch latest prices from the API
        latest_prices = CryptoAPIService.get_latest_prices(list(crypto_ids))
        
        if latest_prices:
            # Update database with latest prices
            for price_data in latest_prices:
                CryptoPrice.objects.create(**price_data)
            
            # Return the latest prices from the database
            latest_prices = CryptoPrice.objects.values('crypto_id').annotate(
                latest_date=models.Max('date')
            )
            return Response(self.serializer_class(
                CryptoPrice.objects.filter(
                    date__in=[p['latest_date'] for p in latest_prices],
                ),
                many=True 
            ).data)
        return Response({"error": "Failed to fetch latest prices"}, status=500)
        
class CryptoMetaDataViewSet(viewsets.ModelViewSet):
    queryset = CryptoMetaData.objects.all()
    serializer_class = CryptoMetaDataSerializer
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        # Fetch trending data from the API
        trending_data = CryptoAPIService.get_trending_cryptos()
        
        if trending_data:
            # Update database with trending data
            for coin_data in trending_data:
                TrendingCrypto.objects.create(**coin_data)
            
            # Return the latest trending data from the database
            trending_data = TrendingCrypto.objects.order_by('-score')[:10]
            return Response(self.serializer_class(trending_data, many=True).data)
        return Response({"error": "Failed to fetch trending data"}, status=500)
    
