import requests

def get_daily_price_change(ticker: str):

    api_key = "KPe2pAHOxYaGTZHJylaCJ3R1oKBfLAd3"

    url = f'https://financialmodelingprep.com/api/v3/stock-price-change/{ticker}?apikey={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        events = response.json()
        price = events[0]['1D']
        return round(float(price), 2)
    else:
        print("Failed to retrieve data")
        return []