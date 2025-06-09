from datetime import datetime
from .models import CryptoPrice, CryptoMetaData, TrendingCrypto
from data_fetch import fetch_crypto, fetch_crypto_metadata, fetch_trending

class CryptoDataService:
    @staticmethod 
    def update_crypto_data(crypto_id):
        try:
            price_data = fetch_crypto(crypto_id, datetime.now().strftime('%d-%m-%Y'))
            metadata = fetch_crypto_metadata(crypto_id)
            
            # TODO: Validate the fetched data
            if not price_data or not metadata:
                raise ValueError(f"No data found for crypto_id: {crypto_id}")
            
            # Update or create database records
            CryptoPrice.objects.update_or_create(
                crypto_id=crypto_id,
                date=datetime.now(),
                defaults={
                    'price_usd': price_data['price_usd'],
                    'market_cap_usd': price_data['market_cap_usd'],
                    'volume_24h_usd': price_data['volume_24h_usd']
                }
            )
            
            CryptoMetaData.objects.update_or_create(
                crypto_id=crypto_id,
                defaults={
                    'name': metadata['name'],
                    'symbol': metadata['symbol'],
                    'description': metadata['description'],
                    'market_cap_rank': metadata['market_cap_rank'],
                    'liquidity_score': metadata['liquidity_score'],
                    'public_interest_score': metadata['public_interest_score'],
                }
            )
            return True
        except Exception as e:
            print(f"Error updating crypto data: {e}")
            return False 
        
        @staticmethod 
        def update_trending_data():
            try:
                trending_data = fetch_trending()
                if not trending_data:
                    raise ValueError("No trending data found")
                
                for coin in trending_data:
                    TrendingCrypto.objects.update_or_create(
                        crypto_id=coin['id'],
                        defaults={
                            'name': coin['name'],
                            'symbol': coin['symbol'],
                            'market_cap_rank': coin['market_cap_rank'],
                            'score': coin['score']
                        }
                    )
                return True
            except Exception as e:
                print(f"Error updating trending data: {e}")
                return False 