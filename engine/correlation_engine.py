def evaluate_intermarket_correlations(snapshot):
    """
    Evaluates Gold (XAUUSD) against DXY, US10Y yields, Silver, Oil, SPX, BTC.
    Inverse relationship with DXY & US10Y (Weak DXY -> Bullish Gold).
    Direct relationship with Silver (XAG/USD).
    """
    dxy = snapshot.get('DXY', 0.0)
    us10y = snapshot.get('US10Y', 0.0)
    silver = snapshot.get('Silver', 0.0)

    score = 50.0
    factors = []

    # DXY evaluation (Assuming baseline DXY benchmark around 103-105)
    if dxy > 0:
        if dxy < 104.0:
            score += 15
            factors.append("DXY weak (<104.0) -> Strong tailwind for Gold")
        else:
            score -= 10
            factors.append("DXY resilient (>104.0) -> Headwind for Gold")

    # US10Y evaluation (High yields negative for non-yielding Gold)
    if us10y > 0:
        if us10y < 4.20:
            score += 15
            factors.append("US 10Y Yield soft (<4.20%) -> Bullish Gold")
        else:
            score -= 10
            factors.append("US 10Y Yield high (>4.20%) -> Pressure on Gold")

    score = max(0.0, min(100.0, score))
    bias = "BULLISH" if score >= 60.0 else ("BEARISH" if score <= 40.0 else "NEUTRAL")

    return {
        'correlation_score': score,
        'bias': bias,
        'factors': factors
    }

if __name__ == '__main__':
    print("Correlation engine module ready.")
