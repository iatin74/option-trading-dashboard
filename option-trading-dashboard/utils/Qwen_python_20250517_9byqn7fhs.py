import pandas as pd

def calculate_gex(options_df):
    options_df['gex'] = (
        options_df['open_interest'] *
        options_df['gamma'] *
        (options_df['strike'] ** 2) *
        0.01
    )
    return options_df[['strike', 'open_interest', 'gamma', 'gex']]

def create_gex_heatmap_data(options_df):
    pivot_table = options_df.pivot_table(
        index='expiration_date',
        columns='strike',
        values='gex',
        aggfunc='sum'
    ).fillna(0)
    return pivot_table