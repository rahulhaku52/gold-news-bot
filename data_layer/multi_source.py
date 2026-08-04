import requests
import time
import urllib3
import numpy as np
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
            if 'price' in data and data['price'] > 1000:
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
    """Fetch live spot price using Yahoo Finance XAUUSD=X ticker (Spot Gold)"""
    tickers = ["XAUUSD=X", "XAUUSD=CC"]
    for sym in tickers:
        try:
            ticker = yf.Ticker(sym)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty and 'Close' in data:
                price = float(data['Close'].iloc[-1])
                if price > 1000:
                    return price, time.time()
        except Exception:
            continue
    return None, None

def fetch_finnhub_price():
    """Fetch spot gold price (OANDA:XAU_USD) from Finnhub if API key is provided"""
    if not config.FINNHUB_KEY:
        return None, None
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol=OANDA:XAU_USD&token={config.FINNHUB_KEY}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if 'c' in data and data['c'] > 1000:
                return float(data['c']), time.time()
    except Exception as e:
        print(f"⚠️ Finnhub price error: {e}")
    return None, None

def fetch_all_spot_prices():
    """
    Collects live spot gold (XAUUSD) prices from 5 independent real-time spot sources.
    Filters out futures contracts (GC=F) or delisted outliers.
    """
    prices = {}

    m_price, m_ts = fetch_metals_live_price()
    if m_price:
        prices['metals_live'] = {'price': m_price, 'timestamp': m_ts}

    g_price, g_ts = fetch_gold_api_price()
    if g_price:
        prices['gold_api'] = {'price': g_price, 'timestamp': g_ts}

    gp_price, gp_ts = fetch_goldprice_org()
    if gp_price:
        prices['goldprice_org'] = {'price': gp_price, 'timestamp': gp_ts}

    y_price, y_ts = fetch_yahoo_spot_price()
    if y_price:
        prices['yahoo_spot'] = {'price': y_price, 'timestamp': y_ts}

    f_price, f_ts = fetch_finnhub_price()
    if f_price:
        prices['finnhub_spot'] = {'price': f_price, 'timestamp': f_ts}

    price_str = ", ".join([f"{k}: ${v['price']:.2f}" for k, v in prices.items()])
    print(f"🔍 DEBUG Spot Prices -> {price_str}")

    # Outlier Filtering: Calculate median of raw prices
    if len(prices) >= 2:
        raw_vals = [info['price'] for info in prices.values()]
        med = float(np.median(raw_vals))
        filtered_prices = {}
        for src, info in prices.items():
            if abs(info['price'] - med) <= 3.0: # Keep only sources within $3 of median
                filtered_prices[src] = info
            else:
                print(f"⚠️ Rejecting Outlier Source '{src}': ${info['price']:.2f} (Median: ${med:.2f})")
        return filtered_prices

    return prices

def fetch_ohlcv_data(symbol=config.SYMBOL_GOLD_SPOT, period="60d", interval="1h"):
    """Fetch multi-timeframe OHLCV historical dataframe (using XAUUSD=X spot ticker)"""
    symbols_to_try = [symbol, "XAUUSD=X", "GC=F"]
    for sym in symbols_to_try:
        try:
            ticker = yf.Ticker(sym)
            df = ticker.history(period=period, interval=interval)
            if not df.empty and len(df) > 20:
                return df
        except Exception:
            continue
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
        price, ts = fetch_yahoo_spot_price() if sym == "XAUUSD=X" else (None, None)
        if not price:
            try:
                t = yf.Ticker(sym)
                h = t.history(period="1d", interval="1m")
                if not h.empty:
                    price = float(h['Close'].iloc[-1])
            except Exception:
                price = 0.0
        snapshot[name] = price if price else 0.0
    return snapshot

if __name__ == '__main__':
    print("Testing 5-source spot price fetch with Outlier Rejection...")
    print("Filtered Spot Prices:", fetch_all_spot_prices())
