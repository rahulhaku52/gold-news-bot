import requests
import time
import urllib3
import yfinance as yf
import pandas as pd
from datetime import datetime
import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_metals_live_price():
    """Fetch live spot XAUUSD gold price from metals.live API"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        resp = requests.get("https://api.metals.live/v1/spot/gold", headers=headers, timeout=5, verify=False)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0 and 'gold' in data[0]:
                return float(data[0]['gold']), time.time()
            elif isinstance(data, dict) and 'price' in data:
                return float(data['price']), time.time()
    except Exception:
        pass
    return None, None

def fetch_gold_api_price():
    """Fetch live spot XAUUSD gold price from gold-api.com"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        resp = requests.get("https://api.gold-api.com/price/XAU", headers=headers, timeout=5, verify=False)
        if resp.status_code == 200:
            data = resp.json()
            if 'price' in data and data['price'] > 0:
                return float(data['price']), time.time()
    except Exception:
        pass
    return None, None

def fetch_goldprice_org():
    """Fetch live spot XAUUSD gold price from data-asg.goldprice.org"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        resp = requests.get("https://data-asg.goldprice.org/dbursa/XAUUSD", headers=headers, timeout=5, verify=False)
        if resp.status_code == 200:
            data = resp.json()
            if 'items' in data and len(data['items']) > 0 and 'xauPrice' in data['items'][0]:
                return float(data['items'][0]['xauPrice']), time.time()
    except Exception:
        pass
    return None, None

def fetch_yahoo_spot_price():
    """Fetch live spot price using Yahoo Finance XAUUSD=X or GC=F ticker"""
    tickers = ["XAUUSD=X", "GC=F"]
    for sym in tickers:
        try:
            ticker = yf.Ticker(sym)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty and 'Close' in data:
                price = float(data['Close'].iloc[-1])
                if price > 0:
                    return price, time.time()
        except Exception:
            continue
    return None, None

def fetch_yahoo_price(symbol=config.SYMBOL_GOLD_FUTURES):
    """Generic Yahoo Finance price fetcher with ticker fallbacks"""
    symbols_to_try = [symbol]
    if symbol == config.SYMBOL_DXY:
        symbols_to_try = config.SYMBOL_DXY_TICKERS

    for sym in symbols_to_try:
        try:
            ticker = yf.Ticker(sym)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty and 'Close' in data:
                latest_price = float(data['Close'].iloc[-1])
                return latest_price, time.time()
        except Exception:
            continue

    return None, None

def fetch_all_spot_prices():
    """
    Collects live spot gold (XAUUSD) prices from 4 independent real-time spot sources.
    """
    prices = {}

    m_price, m_ts = fetch_metals_live_price()
    if m_price and m_price > 1000:
        prices['metals_live'] = {'price': m_price, 'timestamp': m_ts}

    g_price, g_ts = fetch_gold_api_price()
    if g_price and g_price > 1000:
        prices['gold_api'] = {'price': g_price, 'timestamp': g_ts}

    gp_price, gp_ts = fetch_goldprice_org()
    if gp_price and gp_price > 1000:
        prices['goldprice_org'] = {'price': gp_price, 'timestamp': gp_ts}

    y_price, y_ts = fetch_yahoo_spot_price()
    if y_price and y_price > 1000:
        prices['yahoo_spot'] = {'price': y_price, 'timestamp': y_ts}

    return prices

def fetch_ohlcv_data(symbol=config.SYMBOL_GOLD_FUTURES, period="60d", interval="1h"):
    """Fetch multi-timeframe OHLCV historical dataframe"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if df.empty:
            df = yf.download(symbol, period=period, interval=interval, progress=False)
        return df
    except Exception as e:
        print(f"⚠️ Historical fetch error for {symbol} ({interval}): {e}")
        return pd.DataFrame()

def fetch_intermarket_snapshot():
    """Fetch snapshot prices for DXY, US10Y, Silver, Oil, SPX, BTC"""
    symbols = {
        'DXY': config.SYMBOL_DXY,
        'US10Y': config.SYMBOL_US10Y,
        'Silver': config.SYMBOL_SILVER,
        'Oil': config.SYMBOL_OIL,
        'SPX': config.SYMBOL_SPX,
        'BTC': config.SYMBOL_BTC
    }
    snapshot = {}
    for name, sym in symbols.items():
        price, ts = fetch_yahoo_price(sym)
        snapshot[name] = price if price else 0.0
    return snapshot

if __name__ == '__main__':
    print("Testing 4-source spot price fetch...")
    print("Spot prices:", fetch_all_spot_prices())
