from django.test import TestCase
from unittest.mock import patch
from ..services import CryptoDataService
from ..models import CryptoPrice, CryptoMetaData

class CryptoDataServiceTests(TestCase):
    def setUp(self):
        self.test_crypto_id = 'bitcoin'
        self.test_price_data = {
            'price_usd': 50000,
            'market_cap_usd': 1000000000,
            'volume_24h_usd': 500000000
        }
        self.test_metadata = {
            'name': 'Bitcoin',
            'symbol': 'BTC',
            'description': 'Test description',
            'market_cap_rank': 1
        }

    @patch('crypto_api.services.fetch_crypto')
    @patch('crypto_api.services.fetch_crypto_metadata')
    def test_update_crypto_data(self, mock_metadata, mock_price):
        mock_price.return_value = self.test_price_data
        mock_metadata.return_value = self.test_metadata

        result = CryptoDataService.update_crypto_data(self.test_crypto_id)
        self.assertTrue(result)

        price = CryptoPrice.objects.get(crypto_id=self.test_crypto_id)
        self.assertEqual(price.price_usd, self.test_price_data['price_usd']) 