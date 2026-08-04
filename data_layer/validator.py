import time
import numpy as np
import config

def validate_price_freshness(timestamp, max_age_seconds=config.MAX_DATA_AGE_SECONDS):
    """Check if timestamp is fresh (< 60s old)"""
    if not timestamp:
        return False
    age = time.time() - timestamp
    return age <= max_age_seconds

def cross_validate_prices(sources_dict):
    """
    Cross-validates price data across multiple sources.
    Rejects signal if sources mismatch by more than config.MAX_PRICE_MISMATCH_DOLLARS.
    """
    if not sources_dict:
        return None, False, "No price data sources available."

    valid_prices = []
    for source, info in sources_dict.items():
        price = info.get('price')
        ts = info.get('timestamp')
        if price and validate_price_freshness(ts, max_age_seconds=120): # Allow up to 2 min for free tier lag
            valid_prices.append(price)

    if not valid_prices:
        return None, False, "Price feed stale (>60s age). Rejected."

    min_p = min(valid_prices)
    max_p = max(valid_prices)
    spread = max_p - min_p

    if spread > config.MAX_PRICE_MISMATCH_DOLLARS and len(valid_prices) > 1:
        return None, False, f"Price feed inconsistent across sources. Mismatch spread: ${spread:.2f} > ${config.MAX_PRICE_MISMATCH_DOLLARS:.2f}"

    consensus_price = float(np.median(valid_prices))
    return consensus_price, True, "Data validated clean."

def validate_candle_dataframe(df):
    """Check for empty candles, NaN values, zero volume anomalies"""
    if df is None or df.empty:
        return False, "Dataframe empty"
    
    if len(df) < 50:
        return False, f"Insufficient candles ({len(df)} < 50)"

    if df['Close'].isnull().any() or (df['Close'] == 0).any():
        return False, "Dataframe contains null or zero price candles"

    return True, "Candles valid"

if __name__ == '__main__':
    mock_sources = {
        'source_a': {'price': 3384.12, 'timestamp': time.time()},
        'source_b': {'price': 3384.08, 'timestamp': time.time()},
        'source_c': {'price': 3384.11, 'timestamp': time.time()}
    }
    price, valid, msg = cross_validate_prices(mock_sources)
    print(f"Validation Result: Consensus=${price}, Valid={valid}, Msg='{msg}'")
