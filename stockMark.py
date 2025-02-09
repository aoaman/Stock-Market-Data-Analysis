import requests
import json
import sys
from datetime import date
from statistics import mean, median

# Function to get the stock data from the API
def download_data(ticker: str) -> dict:
    ticker = ticker.upper()
    today = date.today()
    start_date = today.replace(year=today.year - 5).strftime('%Y-%m-%d')
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start_date}&limit=9999"
    url = base_url + path
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
