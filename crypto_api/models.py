from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 

# Create your models here.

class CryptoPrice(models.Model):
    def __str__(self):
        return f"{self.crypto_id} - {self.date} - {self.price_usd}"
    
    crypto_id = models.CharField(max_length=100)
    date = models.DateTimeField()
    price_usd = models.FloatField()
    market_cap_usd = models.FloatField(null=True)
    volume_24h_usd = models.FloatField(null=True)
    created_at = models.DateTimeField(default=timezone.now) 
    
    class Meta:
        db_table = 'crypto_prices'
        indexes = [
            models.Index(fields=['crypto_id', 'date']),
        ]

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crypto_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.crypto_ids}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey('CryptoMetaData', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'crypto')
        
    def __str__(self):
        return f"{self.user.username} - {self.crypto.name} ({self.crypto.symbol})"

class CryptoMetaData(models.Model):
    crypto_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    description = models.TextField(null=True)
    market_cap_rank = models.IntegerField(null=True)
    liquidity_score = models.FloatField(null=True)
    public_interest_score = models.FloatField(null=True)
    developer_score = models.FloatField(null=True)
    community_score = models.FloatField(null=True)
    created_at = models.DateTimeField(default=timezone.now) 
    
    class Meta:
        db_table = 'crypto_metadata'
        indexes = [
            models.Index(fields=['crypto_id']),
        ]
        
    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
class TrendingCrypto(models.Model):
    crypto_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    market_cap_rank = models.IntegerField(null=True)
    score = models.FloatField(null=True)
    created_at = models.DateTimeField(default=timezone.now) 
    
    class Meta:
        db_table = 'trending_crypto'
        indexes = [
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return f"{self.name} ({self.symbol}) - Score: {self.score}"
