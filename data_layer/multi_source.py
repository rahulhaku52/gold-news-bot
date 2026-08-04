import requests
import time
import urllib3
import yfinance as yf
import pandas as pd
from datetime import datetime
import config

# Disable urllib3 insecure request warnings for SSL fallback
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_metals_live_price():
    """Fetch spot gold from metals.live or gold-api.com with SSL fallback"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # Primary metals.live endpoint
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

    # Secondary gold-api.com fallback endpoint
    try:
        resp = requests.get("https://api.gold-api.com/price/XAU", headers=headers, timeout=5, verify=False)
        if resp.status_code == 200:
            data = resp.json()
            if 'price' in data and data['price'] > 0:
                return float(data['price']), time.time()
    except Exception:
        pass

    return None, None

def fetch_yahoo_price(symbol=config.SYMBOL_GOLD_FUTURES):
    """Fetch price from Yahoo Finance ticker with fallback tickers"""
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

def fetch_finnhub_price():
    """Fetch gold spot price from Finnhub if API key is provided"""
    if not config.FINNHUB_KEY:
        return None, None
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol=OANDA:XAU_USD&token={config.FINNHUB_KEY}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if 'c' in data and data['c'] > 0:
                return float(data['c']), time.time()
    except Exception as e:
        print(f"⚠️ Finnhub price error: {e}")
    return None, None

def fetch_all_spot_prices():
    """Collect spot gold prices from multiple independent sources with timestamps"""
    prices = {}

    metals_price, metals_ts = fetch_metals_live_price()
    if metals_price:
        prices['metals_live'] = {'price': metals_price, 'timestamp': metals_ts}

    yahoo_price, yahoo_ts = fetch_yahoo_price(config.SYMBOL_GOLD_FUTURES)
    if yahoo_price:
        prices['yahoo_futures'] = {'price': yahoo_price, 'timestamp': yahoo_ts}

    finnhub_price, finnhub_ts = fetch_finnhub_price()
    if finnhub_price:
        prices['finnhub'] = {'price': finnhub_price, 'timestamp': finnhub_ts}

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
    print("Testing multi-source fetch...")
    print("Spot prices:", fetch_all_spot_prices())
    print("Intermarket snapshot:", fetch_intermarket_snapshot())
