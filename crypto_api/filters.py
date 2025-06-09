import django_filters 
from .models import CryptoPrice, CryptoMetaData, TrendingCrypto

class CryptoPriceFilter(django_filters.FilterSet):
    class Meta:
        model = CryptoPrice
        fields = {
            'crypto_id': ['exact'],
            'date': ['gte', 'lte'],
            'price_usd': ['gte', 'lte'],
        }

class CryptoMetaDataFilter(django_filters.FilterSet):
    class Meta:
        model = CryptoMetaData
        fields = {
            'crypto_id': ['exact'],
            'name': ['exact'],
            'symbol': ['exact'],
            'market_cap_rank': ['exact'],
            'liquidity_score': ['gte', 'lte'],
            'public_interest_score': ['gte', 'lte'],
            'developer_score': ['gte', 'lte'],
            'community_score': ['gte', 'lte'],
        }
        
class TrendingCryptoFilter(django_filters.FilterSet):
    class Meta:
        model = TrendingCrypto 
        fields = {
            'crypto_id': ['exact'],
            'name': ['exact'],
            'symbol': ['exact'],
            'market_cap_rank': ['exact'],
            'score': ['gte', 'lte'],
        }
        
