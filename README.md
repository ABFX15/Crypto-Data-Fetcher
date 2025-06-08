# Crypto Data Fetcher

A Python application that fetches cryptocurrency data from the CoinGecko API and processes it using pandas.

## Features

- Fetch current price data for any cryptocurrency
- Get detailed metadata for cryptocurrencies
- View trending cryptocurrencies
- Data processing with pandas for analysis

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd crypto-data
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script to fetch Bitcoin data and trending cryptocurrencies:

```bash
python main.py
```

### Example Output

The script will display:

- Current Bitcoin price data (USD price, market cap, 24h volume)
- Bitcoin metadata (description, rankings, scores)
- List of trending cryptocurrencies
- Top 3 trending cryptocurrencies by score

## API Functions

### `fetch_crypto(crypto_id, date)`

Fetches price data for a specific cryptocurrency on a given date.

```python
data = fetch_crypto("bitcoin", "08-06-2024")
```

### `fetch_crypto_metadata(crypto_id)`

Fetches detailed metadata for a cryptocurrency.

```python
metadata = fetch_crypto_metadata("bitcoin")
```

### `fetch_trending()`

Fetches the current trending cryptocurrencies.

```python
trending = fetch_trending()
```

## Data Structure

The data is returned in pandas DataFrame format, making it easy to:

- Perform data analysis
- Create visualizations
- Export to other formats (CSV, Excel, etc.)

## Dependencies

- requests==2.31.0
- pandas==2.2.0

## Note

This project uses the CoinGecko API. Please be mindful of their rate limits when making requests.
