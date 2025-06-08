import unittest
from data_fetch import fetch_crypto, fetch_crypto_metadata, fetch_trending

class TestFetchPrice(unittest.TestCase):
    def test_fetch_crypto(self):
        price_data = fetch_crypto('bitcoin', '08-06-2024')
        self.assertIsNotNone(price_data)
        self.assertIn('date', price_data)
        self.assertIn('crypto_id', price_data)
        self.assertIn('price_usd', price_data)
        self.assertIn('market_cap_usd', price_data)
        self.assertIn('volume_24h_usd', price_data)
        
    def test_fetch_crypto_metadata(self):
        metadata = fetch_crypto_metadata('bitcoin')
        self.assertIsNotNone(metadata)
        self.assertIn('id', metadata)
        self.assertIn('name', metadata)
        self.assertIn('symbol', metadata)
        self.assertIn('description', metadata)
        self.assertIn('market_cap_rank', metadata)
        self.assertIn('coingecko_rank', metadata)
        self.assertIn('coingecko_score', metadata)
        self.assertIn('liquidity_score', metadata)
        self.assertIn('public_interest_score', metadata)
        self.assertIn('developer_score', metadata)
        self.assertIn('community_score', metadata)
        
    def test_fetch_trending(self):
        trending = fetch_trending()
        self.assertIsNotNone(trending)
        self.assertIsInstance(trending, list)
        if trending:  # If we got any trending coins
            first_coin = trending[0]
            self.assertIn('id', first_coin)
            self.assertIn('name', first_coin)
            self.assertIn('symbol', first_coin)
            self.assertIn('market_cap_rank', first_coin)
            self.assertIn('score', first_coin)

if __name__ == '__main__':
    unittest.main()