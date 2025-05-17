import pandas as pd

def simulate_covered_call(call_df, stock_price, shares=100):
    call_df = call_df[['strike', 'ask']].copy()
    call_df['break_even'] = stock_price - call_df['ask']
    call_df['max_profit'] = (call_df['strike'] - stock_price) + call_df['ask']
    call_df['breakeven_move'] = ((stock_price - call_df['break_even']) / stock_price) * 100
    return call_df.sort_values(by='strike')