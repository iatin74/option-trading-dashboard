# utils/yahoo_finance_api.py

import yfinance as yf
import pandas as pd

def get_options_chain(symbol):
    try:
        ticker = yf.Ticker(symbol)
        options = ticker.options

        if not options:
            return None

        all_data = []
        for expiry in options:
            calls = ticker.option_chain(expiry).calls
            puts = ticker.option_chain(expiry).puts

            calls['expiration_date'] = expiry
            puts['expiration_date'] = expiry

            calls['option_type'] = 'call'
            puts['option_type'] = 'put'

            all_data.append(calls)
            all_data.append(puts)

        full_df = pd.concat(all_data)
        full_df['underlying_price'] = ticker.history(period="1d")["Close"][0]

        return {
            "options": {
                "option": full_df.to_dict(orient="records")
            },
            "expirations": options,
            "underlying_price": full_df['underlying_price'].iloc[0]
        }

    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
