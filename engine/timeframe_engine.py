import pandas as pd
import numpy as np

def analyze_timeframe_trend(df):
    """Analyze trend direction for a single timeframe DataFrame using EMAs & Close alignment"""
    if df is None or df.empty or len(df) < 20:
        return "NEUTRAL"

    close = df['Close']
    ema20 = close.ewm(span=20, adjust=False).mean()
    ema50 = close.ewm(span=50, adjust=False).mean()

    curr_close = close.iloc[-1]
    curr_ema20 = ema20.iloc[-1]
    curr_ema50 = ema50.iloc[-1]

    if curr_close > curr_ema20 and curr_ema20 > curr_ema50:
        return "BULLISH"
    elif curr_close < curr_ema20 and curr_ema20 < curr_ema50:
        return "BEARISH"
    else:
        return "NEUTRAL"

def evaluate_multi_timeframe_alignment(timeframe_dfs):
    """
    Evaluates multi-timeframe trend alignment (M, W, D, 4H, 1H, 30M, 15M, 5M).
    Returns overall trend bias and alignment strength score (0 to 100).
    """
    trends = {}
    total_weights = 0
    bullish_weight = 0
    bearish_weight = 0

    weights_map = {
        'M': 25,
        'W': 20,
        'D': 20,
        '4H': 15,
        '1H': 10,
        '30M': 5,
        '15M': 3,
        '5M': 2
    }

    for tf, df in timeframe_dfs.items():
        t = analyze_timeframe_trend(df)
        trends[tf] = t
        w = weights_map.get(tf, 5)
        total_weights += w
        if t == "BULLISH":
            bullish_weight += w
        elif t == "BEARISH":
            bearish_weight += w

    if total_weights == 0:
        return "NEUTRAL", 50.0, trends

    bullish_score = (bullish_weight / total_weights) * 100
    bearish_score = (bearish_weight / total_weights) * 100

    if bullish_score > 65:
        overall_trend = "BULLISH"
        score = bullish_score
    elif bearish_score > 65:
        overall_trend = "BEARISH"
        score = bearish_score
    else:
        overall_trend = "NEUTRAL"
        score = 50.0

    return overall_trend, round(score, 1), trends

if __name__ == '__main__':
    print("Timeframe engine module ready.")
