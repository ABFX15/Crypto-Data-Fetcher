from django.core.management.base import BaseCommand 
from crypto_api.models import CryptoPrice, CryptoMetaData, TrendingCrypto

class Command(BaseCommand):
    help = "Updates cryptocurrency data from external API"
    
    def handle(self, *args, **options):
        # Get list of cryptocurrencies to update
        crypto_ids = CryptoMetaData.objects.values_list('crypto_id', flat=True)
        
        # Call cryptodataservice methods
        for crypto_id in crypto_ids:
            self.stdout.write(f"Updating data for {crypto_id}")
            CryptoDataService.update_crypto_data(crypto_id)
            self.stdout.write(f"Updated data for {crypto_id}")
            
        self.stdout.write(self.style.SUCCESS("All data updated successfully"))
        
        # log results
        self.stdout.write(self.style.SUCCESS("All data updated successfully"))
        
        # update trending data
        self.stdout.write(self.style.SUCCESS("Updating trending data"))
        CryptoDataService.update_trending_data()
        self.stdout.write(self.style.SUCCESS("Trending data updated successfully"))
        
        # log results
        self.stdout.write(self.style.SUCCESS("All data updated successfully"))