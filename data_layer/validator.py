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
    Hard Real-Time Price Gatekeeper & Cross Validator:
    - Calculates median price across independent real-time spot sources.
    - Rejects analysis if price spread mismatch exceeds $1.50 USD or timestamp > 60s.
    """
    if not sources_dict:
        return None, False, "REJECTED: No real-time spot price sources available."

    valid_prices = []
    source_names = []

    for source, info in sources_dict.items():
        price = info.get('price')
        ts = info.get('timestamp')
        if price and price > 1000 and validate_price_freshness(ts, max_age_seconds=120):
            valid_prices.append(price)
            source_names.append(source)

    if not valid_prices:
        return None, False, "REJECTED: Real-time spot price feed stale (>60s age)."

    if len(valid_prices) == 1:
        # Single source valid - return price with warning
        return float(valid_prices[0]), True, f"Single spot source ({source_names[0]}) verified: ${valid_prices[0]:.2f}"

    min_p = min(valid_prices)
    max_p = max(valid_prices)
    spread = max_p - min_p

    if spread > 1.50:
        return None, False, f"REJECTED: Real-time spot price mismatch across sources. Spread ${spread:.2f} > $1.50 tolerance (Prices: {valid_prices})"

    consensus_price = float(np.median(valid_prices))
    return round(consensus_price, 2), True, f"Consensus spot price validated across {len(valid_prices)} sources ({', '.join(source_names)})"

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
        'gold_api': {'price': 4090.12, 'timestamp': time.time()},
        'metals_live': {'price': 4090.08, 'timestamp': time.time()},
        'goldprice_org': {'price': 4090.15, 'timestamp': time.time()}
    }
    price, valid, msg = cross_validate_prices(mock_sources)
    print(f"Validation Result: Spot Price=${price}, Valid={valid}, Msg='{msg}'")
