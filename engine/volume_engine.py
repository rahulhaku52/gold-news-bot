import numpy as np
import pandas as pd

def analyze_advanced_volume(df):
    """
    Advanced Volume & Microstructure Analysis:
    - Relative Volume (RVOL): Volume / 20-period SMA Volume
    - Volume Absorption: High RVOL (>1.8x) with small candle body at key level
    - Volume Climax: Extreme RVOL (>2.5x) indicating potential exhaustion
    """
    if df is None or df.empty or 'Volume' not in df or len(df) < 20:
        return {'rvol': 1.0, 'is_absorption': False, 'is_climax': False, 'volume_score': 50.0}

    volume = df['Volume']
    close = df['Close']
    open_p = df['Open']
    high = df['High']
    low = df['Low']

    avg_volume20 = volume.rolling(20).mean().iloc[-1]
    curr_vol = volume.iloc[-1]

    rvol = round(curr_vol / avg_volume20, 2) if avg_volume20 > 0 else 1.0

    candle_body = abs(close.iloc[-1] - open_p.iloc[-1])
    candle_range = high.iloc[-1] - low.iloc[-1] if (high.iloc[-1] - low.iloc[-1]) > 0 else 1e-9

    # Absorption: High Volume but small body relative to range (< 35% range)
    is_absorption = (rvol >= 1.6) and ((candle_body / candle_range) < 0.35)

    # Volume Climax: Spike > 2.5x RVOL
    is_climax = (rvol >= 2.5)

    # Volume Score (0 - 100)
    score = 50.0
    if rvol >= 1.5:
        score += 25.0
    elif rvol < 0.7:
        score -= 15.0

    if is_absorption:
        score += 15.0

    return {
        'rvol': rvol,
        'is_absorption': is_absorption,
        'is_climax': is_climax,
        'volume_score': min(100.0, max(0.0, score))
    }

if __name__ == '__main__':
    print("Volume engine module ready.")
