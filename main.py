from data_fetch import fetch_crypto, fetch_crypto_metadata, fetch_trending
from datetime import datetime
import json 
import pandas as pd

def main():
    crypto_id = "bitcoin"
    today = datetime.now().strftime("%d-%m-%Y")
    
    price_data = fetch_crypto(crypto_id, today)
    if price_data:
        price_df = pd.DataFrame([price_data])
        print("\nBitcoin Price data:")
        print(price_df.to_string(index=False))
        
    metadata = fetch_crypto_metadata(crypto_id)
    if metadata:
        metadata_df = pd.DataFrame([metadata])
        print("\nBitcoin Metadata:")
        print(metadata_df.to_string(index=False))
        
    trending = fetch_trending()
    if trending:
        trending_df = pd.DataFrame(trending)
        print("\nTrending Cryptocurrencies:")
        print(trending_df.to_string(index=False))
        
        print("\nTop 3 Trending Cryptocurrencies by Score:")
        top_trending = trending_df.nlargest(3, 'score')
        print(top_trending[['name', 'symbol', 'score']].to_string(index=False))



if __name__ == "__main__":
    main()
