from django.contrib import admin
from .models import CryptoPrice, CryptoMetaData, TrendingCrypto

@admin.register(CryptoPrice)
class CryptoPriceAdmin(admin.ModelAdmin):
    list_display = ('crypto_id', 'date', 'price_usd', 'market_cap_usd', 'volume_24h_usd')
    list_filter = ('crypto_id', 'date')
    search_fields = ('crypto_id',)
    ordering = ('-date',)
    

@admin.register(CryptoMetaData)
class CryptoMetaDataAdmin(admin.ModelAdmin):
    list_display = ('crypto_id', 'name', 'symbol', 'market_cap_rank')
    list_filter = ('market_cap_rank',)
    search_fields = ('crypto_id', 'name', 'symbol')
    ordering = ('market_cap_rank',)
    
@admin.register(TrendingCrypto)
class TrendingCryptoAdmin(admin.ModelAdmin):
    list_display = ('crypto_id', 'name', 'symbol', 'market_cap_rank', 'score')
    list_filter = ('market_cap_rank',)
    search_fields = ('crypto_id', 'name', 'symbol')
    ordering = ('-score',)