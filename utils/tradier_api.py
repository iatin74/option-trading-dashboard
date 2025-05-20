import requests
from config import TRADIER_API_KEY

BASE_URL = "https://sandbox.tradier.com/v1/markets "

def get_options_chain(symbol):
    headers = {
        "Authorization": f"Bearer {TRADIER_API_KEY}",
        "Accept": "application/json"
    }

    url = f"{BASE_URL}/options/chains"
    params = {
        "symbol": symbol,
        "expiration": ""
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            expirations = sorted(set(option['expiration_date'] for option in data['options']['option']))
            data['expirations'] = expirations
            return data
        except Exception as e:
            print(f"Fehler beim Parsen der JSON-Antwort: {e}")
            print(f"Antwort-Inhalt: {response.text}")
            return None
    else:
        print(f"Fehler beim Abrufen der Daten: {response.status_code}")
        print(response.text)
        return None
        import requests
from config import TRADIER_API_KEY

BASE_URL = "https://sandbox.tradier.com/v1/markets "

def get_options_chain(symbol):
    headers = {
        "Authorization": f"Bearer {TRADIER_API_KEY}",
        "Accept": "application/json"
    }

    url = f"{BASE_URL}/options/chains"
    params = {
        "symbol": symbol,
        "expiration": ""
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            expirations = sorted(set(option['expiration_date'] for option in data['options']['option']))
            data['expirations'] = expirations
            return data
        except Exception as e:
            print(f"Fehler beim Parsen der JSON-Antwort: {e}")
            print(f"Antwort-Inhalt: {response.text}")
            return None
    else:
        print(f"Fehler beim Abrufen der Daten: {response.status_code}")
        print(response.text)
        return None
