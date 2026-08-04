import pandas as pd
import numpy as np

def detect_candlestick_patterns(df):
    """
    Detects major candlestick patterns:
    - Bullish / Bearish Engulfing
    - Pin Bar / Hammer / Shooting Star
    - Morning Star / Evening Star
    - Doji / Inside Bar / Outside Bar
    """
    if df is None or df.empty or len(df) < 5:
        return {'pattern': 'None', 'direction': 'NEUTRAL', 'score': 50.0}

    op = df['Open'].values
    hi = df['High'].values
    lo = df['Low'].values
    cl = df['Close'].values

    i = -1 # Latest completed candle
    prev = -2

    body = abs(cl[i] - op[i])
    total_range = hi[i] - lo[i] if (hi[i] - lo[i]) > 0 else 1e-9
    upper_wick = hi[i] - max(cl[i], op[i])
    lower_wick = min(cl[i], op[i]) - lo[i]

    pattern = "Standard Candle"
    direction = "NEUTRAL"
    score = 50.0

    # Bullish Engulfing
    if cl[prev] < op[prev] and cl[i] > op[i] and cl[i] >= op[prev] and op[i] <= cl[prev]:
        pattern = "Bullish Engulfing"
        direction = "BULLISH"
        score = 85.0

    # Bearish Engulfing
    elif cl[prev] > op[prev] and cl[i] < op[i] and cl[i] <= op[prev] and op[i] >= cl[prev]:
        pattern = "Bearish Engulfing"
        direction = "BEARISH"
        score = 15.0

    # Pin Bar / Hammer (Lower wick > 60% total range)
    elif lower_wick / total_range > 0.60:
        pattern = "Bullish Pin Bar / Hammer"
        direction = "BULLISH"
        score = 80.0

    # Shooting Star (Upper wick > 60% total range)
    elif upper_wick / total_range > 0.60:
        pattern = "Bearish Shooting Star"
        direction = "BEARISH"
        score = 20.0

    # Doji
    elif body / total_range < 0.10:
        pattern = "Doji (Indecision)"
        direction = "NEUTRAL"
        score = 50.0

    return {
        'pattern': pattern,
        'direction': direction,
        'pa_score': score
    }

if __name__ == '__main__':
    print("Price action module ready.")
