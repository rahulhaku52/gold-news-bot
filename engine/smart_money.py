import pandas as pd
import numpy as np

def detect_smart_money_concepts(df):
    """
    Detects Order Blocks (OB), Fair Value Gaps (FVG), and Premium/Discount Zones.
    """
    if df is None or df.empty or len(df) < 30:
        return {
            'bullish_ob': None,
            'bearish_ob': None,
            'zone': 'Equilibrium',
            'smc_score': 50.0
        }

    high = df['High'].values
    low = df['Low'].values
    close = df['Close'].values
    open_p = df['Open'].values

    curr_price = close[-1]
    recent_high = max(high[-30:])
    recent_low = min(low[-30:])

    # Premium / Discount / Equilibrium calculation
    eq = (recent_high + recent_low) / 2.0
    range_span = recent_high - recent_low if (recent_high - recent_low) > 0 else 1.0

    relative_pos = (curr_price - recent_low) / range_span

    if relative_pos >= 0.70:
        zone = 'Premium'
    elif relative_pos <= 0.30:
        zone = 'Discount'
    else:
        zone = 'Equilibrium'

    # Order Block Detection (simplified OB logic)
    bullish_ob = None
    bearish_ob = None

    for i in range(len(df) - 5, len(df) - 1):
        # Bullish OB: Bearish candle prior to strong upward impulse
        if close[i] < open_p[i] and close[i + 1] > open_p[i + 1] and (close[i + 1] - open_p[i + 1]) > (open_p[i] - close[i]) * 1.5:
            bullish_ob = {'low': low[i], 'high': high[i], 'index': i}
        # Bearish OB: Bullish candle prior to strong downward impulse
        if close[i] > open_p[i] and close[i + 1] < open_p[i + 1] and (open_p[i + 1] - close[i + 1]) > (close[i] - open_p[i]) * 1.5:
            bearish_ob = {'low': low[i], 'high': high[i], 'index': i}

    # SMC Score (Discount zone + Bullish OB -> high BUY score; Premium + Bearish OB -> high SELL score)
    smc_score = 50.0
    if zone == 'Discount':
        smc_score += 20
        if bullish_ob:
            smc_score += 15
    elif zone == 'Premium':
        smc_score -= 20
        if bearish_ob:
            smc_score -= 15

    return {
        'bullish_ob': bullish_ob,
        'bearish_ob': bearish_ob,
        'recent_high': recent_high,
        'recent_low': recent_low,
        'equilibrium': eq,
        'zone': zone,
        'smc_score': max(0.0, min(100.0, smc_score))
    }

if __name__ == '__main__':
    print("Smart money concepts module ready.")
