import requests
import time
from datetime import datetime, timedelta, timezone
from database import Database
import os

# Initialize database
DATABASE_URL = "postgresql://adam_crypto:crypto@localhost:5432/crypto_data"
db = Database(DATABASE_URL)
db.init_db()

def fetch_crypto_data(crypto_id, days=30):
    """Fetch historical data for a cryptocurrency"""
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process and store price data
        for i in range(len(data['prices'])):
            price_data = {
                'date': datetime.fromtimestamp(data['prices'][i][0] / 1000, tz=timezone.utc),
                'price_usd': data['prices'][i][1],
                'market_cap_usd': data['market_caps'][i][1] if 'market_caps' in data else None,
                'volume_24h_usd': data['total_volumes'][i][1] if 'total_volumes' in data else None
            }
            db.store_price_data(crypto_id, price_data)
            
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {crypto_id}: {e}")
        return False

def fetch_crypto_metadata(crypto_id):
    """Fetch metadata for a cryptocurrency"""
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        metadata = {
            'id': data['id'],
            'name': data['name'],
            'symbol': data['symbol'],
            'description': data.get('description', {}).get('en'),
            'market_cap_rank': data.get('market_cap_rank'),
            'liquidity_score': data.get('liquidity_score'),
            'public_interest_score': data.get('public_interest_score'),
            'developer_score': data.get('developer_score'),
            'community_score': data.get('community_score')
        }
        
        db.store_metadata(metadata)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata for {crypto_id}: {e}")
        return False

def fetch_trending():
    """Fetch trending cryptocurrencies"""
    url = "https://api.coingecko.com/api/v3/search/trending"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        trending_data = []
        for coin in data['coins']:
            trending_data.append({
                'id': coin['item']['id'],
                'name': coin['item']['name'],
                'symbol': coin['item']['symbol'],
                'market_cap_rank': coin['item'].get('market_cap_rank'),
                'score': coin['item'].get('score')
            })
        
        db.store_trending(trending_data)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending data: {e}")
        return False

def main():
    # List of cryptocurrencies to track
    crypto_ids = ['bitcoin', 'ethereum', 'dogecoin']
    
    while True:
        print(f"\nFetching data at {datetime.now()}")
        
        # Fetch trending cryptocurrencies
        if fetch_trending():
            print("Successfully fetched and stored trending data")
        
        # Fetch data for each cryptocurrency
        for crypto_id in crypto_ids:
            if fetch_crypto_metadata(crypto_id):
                print(f"Successfully fetched and stored metadata for {crypto_id}")
            
            if fetch_crypto_data(crypto_id):
                print(f"Successfully fetched and stored price data for {crypto_id}")
            
            # Respect API rate limits
            time.sleep(1)
        
        # Wait for 5 minutes before next update
        print("Waiting 5 minutes before next update...")
        time.sleep(300)

if __name__ == "__main__":
    main()
