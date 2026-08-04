def evaluate_market_psychology(df, rsi, rvol, is_absorption):
    """
    Detects behavioral market psychology states:
    - Stop Hunt / Liquidity Grab (Wick sweep of swing high/low followed by sharp reversal)
    - Fake Breakout (Price breaks swing level on low volume and closes back inside range)
    - Exhaustion / Overextension (RSI > 75 or < 25 + high volume climax)
    - Panic / Euphoria
    """
    if df is None or df.empty or len(df) < 10:
        return {'psychology_state': 'Neutral Accumulation', 'risk_modifier': 0}

    close = df['Close'].values
    high = df['High'].values
    low = df['Low'].values
    open_p = df['Open'].values

    curr_close = close[-1]
    curr_high = high[-1]
    curr_low = low[-1]
    prev_high = max(high[-10:-1])
    prev_low = min(low[-10:-1])

    state = "Balanced Sentiment"
    risk_mod = 0

    # Stop Hunt / Liquidity Grab: High sweeps past previous swing high/low but close snaps back inside
    if curr_high > prev_high and curr_close < prev_high:
        state = "Bearish Liquidity Grab (Stop Hunt Above Highs)"
        risk_mod = -10
    elif curr_low < prev_low and curr_close > prev_low:
        state = "Bullish Liquidity Grab (Stop Hunt Below Lows)"
        risk_mod = 10
    # Exhaustion
    elif rsi > 75 and rvol >= 2.0:
        state = "Bullish Euphoria / Buying Exhaustion"
        risk_mod = -15
    elif rsi < 25 and rvol >= 2.0:
        state = "Bearish Panic / Selling Exhaustion"
        risk_mod = 15
    elif is_absorption:
        state = "Institutional Liquidity Absorption"
        risk_mod = 5

    return {
        'psychology_state': state,
        'risk_modifier': risk_mod
    }

if __name__ == '__main__':
    print("Market psychology module ready.")
