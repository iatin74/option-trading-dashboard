import streamlit as st

WATCHLIST_KEY = "option_watchlist"

def load_watchlist():
    return st.session_state.get(WATCHLIST_KEY, [])

def save_to_watchlist(symbol):
    watchlist = load_watchlist()
    if symbol not in watchlist:
        watchlist.append(symbol)
    st.session_state[WATCHLIST_KEY] = watchlist

def remove_from_watchlist(symbol):
    watchlist = load_watchlist()
    if symbol in watchlist:
        watchlist.remove(symbol)
    st.session_state[WATCHLIST_KEY] = watchlist