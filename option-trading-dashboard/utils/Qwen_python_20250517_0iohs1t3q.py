import pandas as pd

def calculate_dix_dex(calls_df, puts_df):
    total_call_volume = calls_df['volume'].sum()
    total_put_volume = puts_df['volume'].sum()
    total_call_oi = calls_df['open_interest'].sum()
    total_put_oi = puts_df['open_interest'].sum()

    dix = total_call_volume / total_put_volume if total_put_volume > 0 else float('inf')
    dex = total_call_oi / total_put_oi if total_put_oi > 0 else float('inf')

    return {
        'dix': dix,
        'dex': dex,
        'call_volume': total_call_volume,
        'put_volume': total_put_volume,
        'call_oi': total_call_oi,
        'put_oi': total_put_oi
    }