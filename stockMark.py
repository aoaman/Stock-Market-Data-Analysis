"""
Author: Asher Adighije
Date: 2025-02-08
Description: This program is a simple stock market analysis tool that uses the NASDAQ API to get stock data for a given ticker symbol. The program calculates the mean and median closing prices for the last 5 years and prints the results to the console.

Sources: 
ChatGPT: helped with debugging the code specifically the with the fe
"""
import requests
import json
import sys
import time
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
    
    retries = 3 # Number of retries in case of failure implemented cause I was getting errors
    for attempt in range(retries):
        try:
            start_time = time.time() # this is cause I kept getting errors
            response = requests.get(url, headers=headers, timeout=30)
            end_time = time.time() 
            # since I was getting errors I wanted to see how long it took to get the data
            print(f"Request time for {ticker}: {end_time - start_time:.2f} seconds")
            response.raise_for_status()

            data = response.json()
            # Check if the data is valid
            if 'data' not in data or 'tradesTable' not in data['data'] or 'rows' not in data['data']['tradesTable']:
                raise ValueError(f"No valid data found for {ticker}")
            # Extract the closing prices from the data
            closing_prices = [
                float(row['close'].replace("$", "").replace(",", "")) # this is to remove the $ and , from the data which was causing errors
                for row in data['data']['tradesTable']['rows']
                if 'close' in row and row['close']
            ]
            # Check if closing prices are available
            if not closing_prices:
                raise ValueError(f"No closing prices available for {ticker}")
            # Calculate the min, max, mean, and median closing prices
            stats = {
                "ticker": ticker,
                "min": min(closing_prices),
                "max": max(closing_prices),
                "avg": mean(closing_prices),
                "median": median(closing_prices)
            }

            return stats
        # Handle exceptions
        except (requests.RequestException, ValueError) as e:
            print(f"Attempt {attempt + 1} failed for {ticker}: {e}")
            if attempt == retries - 1:
                return {"error": str(e), "ticker": ticker}
            time.sleep(2)