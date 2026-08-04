import pandas as pd
import numpy as np

def detect_market_structure(df, swing_length=5):
    """
    LuxAlgo Smart Money Concepts translation to Python:
    - Swing Points (HH, HL, LH, LL)
    - Break of Structure (BOS)
    - Change of Character (CHoCH)
    - Equal Highs (EQH) / Equal Lows (EQL)
    - Structural Bias & Confluence Score
    """
    if df is None or df.empty or len(df) < (swing_length * 2 + 10):
        return {
            'structure_bias': 'NEUTRAL',
            'last_event': 'NONE',
            'swing_highs': [],
            'swing_lows': [],
            'eqh': False,
            'eql': False,
            'structure_score': 50.0
        }

    high = df['High'].values
    low = df['Low'].values
    close = df['Close'].values

    n = len(df)
    swing_highs = []
    swing_lows = []

    # Swing detection loop
    for i in range(swing_length, n - swing_length):
        if high[i] == max(high[i - swing_length : i + swing_length + 1]):
            swing_highs.append({'index': i, 'price': high[i]})
        if low[i] == min(low[i - swing_length : i + swing_length + 1]):
            swing_lows.append({'index': i, 'price': low[i]})

    if not swing_highs or not swing_lows:
        return {'structure_bias': 'NEUTRAL', 'last_event': 'NONE', 'structure_score': 50.0}

    last_sh = swing_highs[-1]['price']
    last_sl = swing_lows[-1]['price']
    prev_sh = swing_highs[-2]['price'] if len(swing_highs) > 1 else last_sh
    prev_sl = swing_lows[-2]['price'] if len(swing_lows) > 1 else last_sl

    curr_price = close[-1]
    bias = 'NEUTRAL'
    last_event = 'CONSOLIDATION'

    # BOS and CHoCH detection
    if curr_price > last_sh:
        bias = 'BULLISH'
        last_event = 'BOS' if prev_sh < last_sh else 'CHoCH'
    elif curr_price < last_sl:
        bias = 'BEARISH'
        last_event = 'BOS' if prev_sl > last_sl else 'CHoCH'
    else:
        if last_sh > prev_sh and last_sl > prev_sl:
            bias = 'BULLISH'
        elif last_sh < prev_sh and last_sl < prev_sl:
            bias = 'BEARISH'

    # Equal Highs (EQH) / Equal Lows (EQL) detection
    atr = np.mean(high[-14:] - low[-14:])
    threshold = 0.15 * atr
    eqh = len(swing_highs) >= 2 and abs(swing_highs[-1]['price'] - swing_highs[-2]['price']) < threshold
    eql = len(swing_lows) >= 2 and abs(swing_lows[-1]['price'] - swing_lows[-2]['price']) < threshold

    # Structure Score (0 - 100)
    score = 50.0
    if bias == 'BULLISH':
        score = 80.0 if last_event in ['BOS', 'CHoCH'] else 65.0
    elif bias == 'BEARISH':
        score = 20.0 if last_event in ['BOS', 'CHoCH'] else 35.0

    return {
        'structure_bias': bias,
        'last_event': last_event,
        'last_swing_high': last_sh,
        'last_swing_low': last_sl,
        'eqh': eqh,
        'eql': eql,
        'structure_score': score
    }

if __name__ == '__main__':
    print("Market structure SMC module ready.")
