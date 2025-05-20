# utils/finnhub_api.py

import requests
from config import FINNHUB_API_KEY

def get_options_chain(symbol):
    """
    Holt die Optionskette für einen gegebenen Ticker von der Finnhub API.
    
    :param symbol: Der Ticker-Symbol (z. B. 'SPX', 'AAPL')
    :return: JSON-Daten mit Optionsdaten oder None bei Fehler
    """
    url = f"https://finnhub.io/api/v1/stock/option-chain?symbol= {symbol}&token={FINNHUB_API_KEY}"
    
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except Exception as e:
            print(f"Fehler beim Parsen der JSON-Antwort: {e}")
            print(f"Antwort-Inhalt: {response.text}")
            return None
    else:
        print(f"Fehler beim Abrufen der Daten: {response.status_code}")
        print(response.text)
        return None
