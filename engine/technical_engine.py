import pandas as pd
import numpy as np

def compute_rsi(close, window=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))

def compute_technical_indicators(df, current_spot_price=None):
    """
    Computes 100% dynamic technical indicators for a given DataFrame:
    EMA20, EMA50, EMA200, RSI(14), MACD(12,26,9), ATR(14), Bollinger Bands(20,2), Pivot Points.
    Aligns and scales levels directly to current_spot_price if provided.
    """
    if df is None or df.empty or len(df) < 50:
        return {}

    close = df['Close']
    high = df['High']
    low = df['Low']

    # Scale adjustment if OHLCV candle baseline differs from spot price
    candle_close = close.iloc[-1]
    scale_ratio = (current_spot_price / candle_close) if current_spot_price and candle_close > 0 else 1.0

    scaled_close = close * scale_ratio
    scaled_high = high * scale_ratio
    scaled_low = low * scale_ratio

    current_price = current_spot_price if current_spot_price else round(float(scaled_close.iloc[-1]), 2)

    # Calculate Moving Averages on historical scaled candles
    ema20 = round(float(scaled_close.ewm(span=20, adjust=False).mean().iloc[-1]), 2)
    ema50 = round(float(scaled_close.ewm(span=50, adjust=False).mean().iloc[-1]), 2)
    ema200 = round(float(scaled_close.ewm(span=200, adjust=False).mean().iloc[-1]), 2) if len(scaled_close) >= 200 else ema50

    # RSI
    rsi_series = compute_rsi(scaled_close, 14)
    rsi_val = round(float(rsi_series.iloc[-1]), 1) if not rsi_series.empty else 50.0

    # MACD
    ema12 = scaled_close.ewm(span=12, adjust=False).mean()
    ema26 = scaled_close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - signal_line

    # ATR
    tr = np.maximum(scaled_high - scaled_low, np.maximum(abs(scaled_high - scaled_close.shift(1)), abs(scaled_low - scaled_close.shift(1))))
    atr14 = round(float(tr.rolling(14).mean().iloc[-1]), 2)

    # Bollinger Bands
    sma20 = float(scaled_close.rolling(20).mean().iloc[-1])
    std20 = float(scaled_close.rolling(20).std().iloc[-1])
    bb_upper = round(sma20 + (2 * std20), 2)
    bb_lower = round(sma20 - (2 * std20), 2)

    # Dynamic Pivot Points (Standard Daily / Weekly)
    prev_h = float(scaled_high.iloc[-2])
    prev_l = float(scaled_low.iloc[-2])
    prev_c = float(scaled_close.iloc[-2])
    pivot = (prev_h + prev_l + prev_c) / 3.0
    r1 = round((2 * pivot) - prev_l, 2)
    s1 = round((2 * pivot) - prev_h, 2)
    r2 = round(pivot + (prev_h - prev_l), 2)
    s2 = round(pivot - (prev_h - prev_l), 2)

    # Sanity validation: Ensure R1 > current_price and S1 < current_price
    if r1 <= current_price:
        r1 = round(current_price + (atr14 * 1.5), 2)
        r2 = round(current_price + (atr14 * 3.0), 2)
    if s1 >= current_price:
        s1 = round(current_price - (atr14 * 1.5), 2)
        s2 = round(current_price - (atr14 * 3.0), 2)

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

    if float(macd_hist.iloc[-1]) > 0 and float(macd_line.iloc[-1]) > float(signal_line.iloc[-1]):
        score += 15
    elif float(macd_hist.iloc[-1]) < 0 and float(macd_line.iloc[-1]) < float(signal_line.iloc[-1]):
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
        "macd_val": float(macd_line.iloc[-1]),
        "macd_signal": float(signal_line.iloc[-1]),
        "macd_hist": float(macd_hist.iloc[-1]),
        "atr": atr14,
        "bb_upper": bb_upper,
        "bb_lower": bb_lower,
        "pivot": round(pivot, 2),
        "r1": r1,
        "s1": s1,
        "r2": r2,
        "s2": s2,
        "technical_score": score
    }

if __name__ == '__main__':
    print("Technical engine module ready.")
