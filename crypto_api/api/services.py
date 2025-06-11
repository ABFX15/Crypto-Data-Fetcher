import requests
from datetime import datetime, timezone
from typing import Dict, List, Optional
from django.conf import settings

class CryptoAPIService:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    @classmethod
    def get_crypto_price(cls, crypto_id: str, date: str) -> Optional[Dict]:
        """Fetch historical price data for a specific cryptocurrency."""
        url = f"{cls.BASE_URL}/coins/{crypto_id}/history"
        params = {"date": date}
        headers = {"accept": "application/json"}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            market_data = data.get('market_data', {})
            current_price = market_data.get('current_price', {})
            market_cap = market_data.get('market_cap', {})
            total_volume = market_data.get('total_volume', {})
            
            return {
                'date': date,
                'crypto_id': crypto_id,
                'price_usd': current_price.get('usd'),
                'market_cap_usd': market_cap.get('usd'),
                'volume_24h_usd': total_volume.get('usd')
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching price data: {e}")
            return None

    @classmethod
    def get_crypto_metadata(cls, crypto_id: str) -> Optional[Dict]:
        """Fetch metadata for a specific cryptocurrency."""
        url = f"{cls.BASE_URL}/coins/{crypto_id}"
        headers = {"accept": "application/json"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            return {
                'id': data.get('id'),
                'symbol': data.get('symbol'),
                'name': data.get('name'),
                'description': data.get('description', {}).get('en', ''),
                'market_cap_rank': data.get('market_cap_rank'),
                'coingecko_rank': data.get('coingecko_rank'),
                'coingecko_score': data.get('coingecko_score'),
                'liquidity_score': data.get('liquidity_score'),
                'public_interest_score': data.get('public_interest_score'),
                'developer_score': data.get('developer_score'),
                'community_score': data.get('community_score')
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching metadata: {e}")
            return None

    @classmethod
    def get_trending_cryptos(cls) -> Optional[List[Dict]]:
        """Fetch trending cryptocurrencies."""
        url = f"{cls.BASE_URL}/search/trending"
        headers = {"accept": "application/json"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            trending_coins = []
            for coin in data.get('coins', []):
                item = coin.get('item', {})
                coin_data = {
                    'id': item.get('id'),
                    'name': item.get('name'),
                    'symbol': item.get('symbol'),
                    'market_cap_rank': item.get('market_cap_rank'),
                    'score': item.get('score', 0)
                }
                trending_coins.append(coin_data)
            return trending_coins
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trending data: {e}")
            return None

    @classmethod
    def get_latest_prices(cls, crypto_ids: List[str]) -> Optional[List[Dict]]:
        """Fetch latest prices for multiple cryptocurrencies."""
        url = f"{cls.BASE_URL}/simple/price"
        params = {
            "ids": ",".join(crypto_ids),
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }
        headers = {"accept": "application/json"}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            prices = []
            for crypto_id, price_data in data.items():
                prices.append({
                    'crypto_id': crypto_id,
                    'price_usd': price_data.get('usd'),
                    'market_cap_usd': price_data.get('usd_market_cap'),
                    'volume_24h_usd': price_data.get('usd_24h_vol'),
                    'date': datetime.now(timezone.utc)
                })
            return prices
        except requests.exceptions.RequestException as e:
            print(f"Error fetching latest prices: {e}")
            return None 