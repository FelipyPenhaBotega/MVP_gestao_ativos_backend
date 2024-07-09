import requests
from config import Config
import csv
import io
from datetime import datetime

def get_stock_quote(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={Config.ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {data}")
        global_quote = data.get("Global Quote", {})
        if (price := global_quote.get("05. price")) is not None:
            return price
        else:
            print(f"No data found for symbol: {symbol}")
            return None
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        return None

def get_all_symbols():
    url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={Config.ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.text
        print(f"Response Data: {data}")
        symbols = []
        csv_reader = csv.DictReader(io.StringIO(data))
        for row in csv_reader:
            try:
                ipo_date = datetime.strptime(row["ipoDate"], '%Y-%m-%d')
            except ValueError:
                continue  # Skip rows with invalid date format
            if row["exchange"] == "BATS" and row["assetType"] == "ETF" and ipo_date < datetime(2005, 1, 1):
                symbols.append({"symbol": row["symbol"], "name": row["name"]})
        return symbols
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        return []



'''
import csv
from datetime import datetime



# Mock data for stock quotes
mock_stock_data = {
    "AAPL": "150.25",
    "GOOGL": "2750.60",
    "MSFT": "270.34",
}

# Mock data for symbols
mock_symbols_data = [
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corporation"},
]

def get_stock_quote(symbol):
    if symbol in mock_stock_data:
        return mock_stock_data[symbol]
    else:
        print(f"No data found for symbol: {symbol}")
        return None

def get_all_symbols():
    return mock_symbols_data
'''
