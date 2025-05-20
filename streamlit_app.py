import streamlit as st
import pandas as pd
from utils.finnhub_api import get_options_chain
from utils.gex_calculator import calculate_gex, create_gex_heatmap_data
from utils.dix_dex_calculator import calculate_dix_dex
from utils.greeks_visualizer import plot_greeks_by_strike, plot_gex_heatmap
from utils.watchlist_manager import load_watchlist, save_to_watchlist, remove_from_watchlist
from utils.strategy_simulator import simulate_covered_call
import plotly.express as px

st.set_page_config(page_title="📈 Option Trading Dashboard", layout="wide")
st.title("📈 Option Trading Dashboard")

# --- Sidebar: Watchlist ---
with st.sidebar:
    st.header("🔍 Watchlist")
    new_ticker = st.text_input("Ticker hinzufügen (z.B. AAPL)", value="")
    if st.button("Hinzufügen") and new_ticker:
        save_to_watchlist(new_ticker.upper())

    watchlist = load_watchlist()
    for ticker in watchlist:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"• {ticker}")
        with col2:
            if st.button("❌", key=f"rm_{ticker}"):
                remove_from_watchlist(ticker)

symbol = st.text_input("Aktien-/Index-Ticker eingeben (z.B. SPX oder AAPL)", value="SPX")

if st.button("Optionsdaten laden"):
    with st.spinner("Lade Daten von Tradier..."):
        data = get_options_chain(symbol.upper())

        if data and 'options' in data['options']:
            options_data = data['options']['option']
            df = pd.DataFrame(options_data)

            expirations = data.get('expirations', [])
            selected_expiry = st.selectbox("Wähle Expiry Date", expirations)

            df_filtered = df[df['expiration_date'] == selected_expiry]
            calls = df_filtered[df_filtered['option_type'] == 'call']
            puts = df_filtered[df_filtered['option_type'] == 'put']

            st.success(f"✅ Erfolgreich {len(df_filtered)} Optionen für {symbol.upper()} geladen (Expiry: {selected_expiry})")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Gamma Exposure (GEX)", "DIX / DEX", "Greeks", "Strategie", "Rohdaten"])

            # --- Tab 1: GEX ---
            with tab1:
                st.subheader("🧮 Gamma Exposure (GEX) Analyse")
                gex_df = calculate_gex(calls)
                gex_summary = gex_df.groupby('strike').agg({'gex': 'sum'}).sort_values(by='gex', ascending=False).reset_index()

                fig = px.bar(gex_summary, x='strike', y='gex', title=f"GEX – {symbol.upper()} | Expiry: {selected_expiry}", log_y=True)
                st.plotly_chart(fig)

                st.subheader("🌡️ GEX Heatmap (über Expiries)")
                full_gex_df = calculate_gex(df[df['option_type'] == 'call'])
                heatmap_data = create_gex_heatmap_data(full_gex_df)
                fig_heatmap = plot_gex_heatmap(heatmap_data, title=f"GEX Heatmap – {symbol.upper()}")
                st.plotly_chart(fig_heatmap)

            # --- Tab 2: DIX / DEX ---
            with tab2:
                st.subheader("📉 Demand Index (DIX) & Delta Exposure (DEX)")
                stats = calculate_dix_dex(calls, puts)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("DIX (Call Vol / Put Vol)", f"{stats['dix']:.2f}")
                    st.write(f"Call Volume: {stats['call_volume']}")
                    st.write(f"Put Volume: {stats['put_volume']}")

                with col2:
                    st.metric("DEX (Call OI / Put OI)", f"{stats['dex']:.2f}")
                    st.write(f"Call Open Interest: {stats['call_oi']}")
                    st.write(f"Put Open Interest: {stats['put_oi']}")

            # --- Tab 3: Greeks ---
            with tab3:
                st.subheader("🌀 Greeks über Strike Preise")
                greek_options = ['delta', 'gamma', 'theta', 'vega']
                selected_greek = st.selectbox("Wähle Greek", greek_options, key="greek_select")
                fig = plot_greeks_by_strike(df_filtered, greek=selected_greek, title=f"{selected_greek.capitalize()} über Strike Prices | Expiry: {selected_expiry}")
                st.plotly_chart(fig)

            # --- Tab 4: Strategie-Simulator ---
            with tab4:
                st.subheader("🛡️ Covered Call Simulator")
                stock_price = float(st.number_input("Aktueller Kurs", value=df_filtered['underlying_price'].iloc[0]))
                shares = int(st.number_input("Anzahl der Shares", value=100))

                if st.button("Simulieren"):
                    simulation = simulate_covered_call(calls, stock_price=stock_price, shares=shares)
                    st.dataframe(simulation)

                    best_trade = simulation.sort_values(by='max_profit', ascending=False).iloc[0]
                    alert_msg = (
                        f"*🎯 Beste Covered Call Opportunity*\n"
                        f"Strike: `{best_trade.name}`\n"
                        f"Max Profit: `${best_trade['max_profit']:.2f}`\n"
                        f"Break Even: `${best_trade['break_even']:.2f}`\n"
                        f"Symbol: `{symbol.upper()}` | Expiry: `{selected_expiry}`"
                    )

                    if st.checkbox("Telegram Alert senden?"):
                        from utils.telegram_alerts import send_telegram_message
                        if send_telegram_message(alert_msg):
                            st.success("✅ Nachricht erfolgreich per Telegram gesendet!")
                        else:
                            st.warning("❌ Fehler beim Senden der Telegram Nachricht.")

            # --- Tab 5: Rohdaten ---
            with tab5:
                st.subheader("Raw Call Data")
                st.dataframe(calls[['symbol', 'strike', 'expiration_date', 'bid', 'ask', 'last', 'volume', 'open_interest', 'delta', 'gamma', 'theta', 'vega']])

                st.subheader("Raw Put Data")
                st.dataframe(puts[['symbol', 'strike', 'expiration_date', 'bid', 'ask', 'last', 'volume', 'open_interest', 'delta', 'gamma', 'theta', 'vega']])
        else:
            st.warning("Keine Optionsdaten gefunden.")
