'''
Fetching data for crypto assets 
'''
import json 
import requests 
from datetime import datetime


def fetch_crypto(crypto_id, date):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/history"
    params = {
        "date": date
    }
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        market_data = data.get('market_data', {})
        current_price = market_data.get('current_price', {})
        market_cap = market_data.get('market_cap', {})
        total_volume = market_data.get('total_volume', {})
        
        price_data = {
            'date': date,
            'crypto_id': crypto_id,
            'price_usd': current_price.get('usd'),
            'market_cap_usd': market_cap.get('usd'),
            'volume_24h_usd': total_volume.get('usd')
        }
        return price_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None 


def fetch_crypto_metadata(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        metadata = {
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
        return metadata
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return None 

def fetch_trending():
    url = "https://api.coingecko.com/api/v3/search/trending"
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
