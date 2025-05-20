import plotly.express as px

def plot_greeks_by_strike(options_df, greek='gamma', title=""):
    grouped = options_df.groupby('strike')[greek].mean().reset_index()
    fig = px.line(grouped, x='strike', y=greek, title=title)
    return fig

def plot_gex_heatmap(gex_pivot, title="Gamma Exposure Heatmap"):
    fig = px.imshow(
        gex_pivot,
        labels=dict(x="Strike", y="Expiry", color="GEX"),
        title=title,
        aspect="auto"
    )
    fig.update_xaxes(side="top")
    return fig
