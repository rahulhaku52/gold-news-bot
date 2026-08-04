import pandas as pd
import numpy as np

def compute_rsi(close, window=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))

def compute_technical_indicators(df):
    """
    Computes technical indicators for a given DataFrame:
    EMA20, EMA50, EMA200, RSI(14), MACD(12,26,9), ATR(14), Bollinger Bands(20,2), Pivot Points
    """
    if df is None or df.empty or len(df) < 50:
        return {}

    close = df['Close']
    high = df['High']
    low = df['Low']

    # Moving Averages
    ema20 = close.ewm(span=20, adjust=False).mean().iloc[-1]
    ema50 = close.ewm(span=50, adjust=False).mean().iloc[-1]
    ema200 = close.ewm(span=200, adjust=False).mean().iloc[-1] if len(close) >= 200 else ema50

    # RSI
    rsi_series = compute_rsi(close, 14)
    rsi_val = rsi_series.iloc[-1] if not rsi_series.empty else 50.0

    # MACD
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - signal_line

    # ATR
    tr = np.maximum(high - low, np.maximum(abs(high - close.shift(1)), abs(low - close.shift(1))))
    atr14 = tr.rolling(14).mean().iloc[-1]

    # Bollinger Bands
    sma20 = close.rolling(20).mean().iloc[-1]
    std20 = close.rolling(20).std().iloc[-1]
    bb_upper = sma20 + (2 * std20)
    bb_lower = sma20 - (2 * std20)

    # Pivot Points (Standard)
    prev_h = high.iloc[-2]
    prev_l = low.iloc[-2]
    prev_c = close.iloc[-2]
    pivot = (prev_h + prev_l + prev_c) / 3.0
    r1 = (2 * pivot) - prev_l
    s1 = (2 * pivot) - prev_h
    r2 = pivot + (prev_h - prev_l)
    s2 = pivot - (prev_h - prev_l)

    current_price = close.iloc[-1]

    # RSI condition
    if rsi_val > 70:
        rsi_bias = "OVERBOUGHT"
    elif rsi_val < 30:
        rsi_bias = "OVERSOLD"
    else:
        rsi_bias = "NEUTRAL"

    # Momentum Alignment Score (0-100)
    score = 50.0
    if current_price > ema20 > ema50:
        score += 20
    elif current_price < ema20 < ema50:
        score -= 20

    if macd_hist.iloc[-1] > 0 and macd_line.iloc[-1] > signal_line.iloc[-1]:
        score += 15
    elif macd_hist.iloc[-1] < 0 and macd_line.iloc[-1] < signal_line.iloc[-1]:
        score -= 15

    if 40 <= rsi_val <= 65 and current_price > ema20:
        score += 15
    elif 35 <= rsi_val <= 60 and current_price < ema20:
        score -= 15

    score = max(0.0, min(100.0, score))

    return {
        "price": current_price,
        "ema20": ema20,
        "ema50": ema50,
        "ema200": ema200,
        "rsi": rsi_val,
        "rsi_bias": rsi_bias,
        "macd_val": macd_line.iloc[-1],
        "macd_signal": signal_line.iloc[-1],
        "macd_hist": macd_hist.iloc[-1],
        "atr": atr14,
        "bb_upper": bb_upper,
        "bb_lower": bb_lower,
        "pivot": pivot,
        "r1": r1,
        "s1": s1,
        "r2": r2,
        "s2": s2,
        "technical_score": score
    }

if __name__ == '__main__':
    print("Technical engine module ready.")
