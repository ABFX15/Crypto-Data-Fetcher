from django.db import models
from django.utils import timezone

class APICall(models.Model):
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    response_time = models.FloatField()
    status_code = models.IntegerField() 
    timestamp = models.DateeTimeField(default=timezone.now) 
    
class DataUpdate(models.Model):
    crypto_id = models.CharField(max_length=100)
    update_type = models.CharField(max_length=50)
    success = models.BooleanField()
    error_message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now) 
    
class APIError(models.Model):
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    error_message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now) 
    
class DataUpdateError(models.Model):
    crypto_id = models.CharField(max_length=100)
    update_type = models.CharField(max_length=50)