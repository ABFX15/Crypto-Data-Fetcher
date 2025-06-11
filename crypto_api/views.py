from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter
from django.db.models import Max, Min
from .models import CryptoPrice, CryptoMetaData, TrendingCrypto
from .serializers import CryptoPriceSerializer, CryptoMetaDataSerializer, TrendingCryptoSerializer
from .filters import CryptoPriceFilter, CryptoMetaDataFilter, TrendingCryptoFilter

class CryptoPriceViewSet(viewsets.ModelViewSet):
    queryset = CryptoPrice.objects.all()
    serializer_class = CryptoPriceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CryptoPriceFilter
    search_fields = ['crypto_id', 'date']
    ordering_fields = ['date', 'price_usd']
    ordering = ['-date']

class CryptoMetaDataViewSet(viewsets.ModelViewSet):
    queryset = CryptoMetaData.objects.all()
    serializer_class = CryptoMetaDataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CryptoMetaDataFilter
    search_fields = ['crypto_id', 'name', 'symbol']
    ordering_fields = ['market_cap_rank', 'liquidity_score', 'public_interest_score', 'developer_score', 'community_score']
    ordering = ['market_cap_rank']
    
class TrendingCryptoViewSet(viewsets.ModelViewSet):
    queryset = TrendingCrypto.objects.all()
    serializer_class = TrendingCryptoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_class = TrendingCryptoFilter
    search_fields = ['crypto_id', 'name', 'symbol']
    ordering_fields = ['market_cap_rank', 'score']
    ordering = ['-score']
    
class DashboardView(TemplateView):
    template_name = 'crypto_api/dashboard.html'

    def get_context_data(self, **kwargs):
        print("Dashboard view called!")  # Debug print
        context = super().get_context_data(**kwargs)
        
        try:
            # Get trending cryptocurrencies
            context['trending_cryptos'] = TrendingCrypto.objects.all().order_by('-score')[:10] or []
            
            # Get latest prices with additional data
            context['latest_prices'] = CryptoPrice.objects.all().order_by('-date')[:5] or []
            
            # Get price history for the chart
            context['price_history'] = CryptoPrice.objects.all().order_by('date')[:100] or []
            
            # Get market cap data
            context['market_caps'] = CryptoPrice.objects.values('crypto_id').annotate(
                total_market_cap=Max('market_cap_usd')
            ).order_by('-total_market_cap')[:5] or []
        except Exception as e:
            print(f"Error fetching data: {e}")
            context['trending_cryptos'] = []
            context['latest_prices'] = []
            context['price_history'] = []
            context['market_caps'] = []
        
        return context
    
    
