def generate_trade_plan(price, direction, atr, swing_high, swing_low):
    """
    Generates exact institutional Trade Plan:
    - Entry Zone (Best Entry, Aggressive, Safe)
    - Stop Loss & Emergency Stop Loss
    - Take Profit Targets (TP1, TP2, TP3, Swing TP)
    - Risk & Reward Metrics
    """
    if atr is None or atr <= 0:
        atr = 12.0 # Standard fallback ATR for Gold

    buffer = atr * 0.8

    if direction == "BUY":
        best_entry = price
        entry_low = round(price - (atr * 0.2), 2)
        entry_high = round(price + (atr * 0.1), 2)

        stop_loss = round(swing_low - buffer if swing_low else (price - (atr * 1.5)), 2)
        emergency_sl = round(stop_loss - (atr * 0.5), 2)

        sl_distance = price - stop_loss
        if sl_distance <= 0:
            sl_distance = atr * 1.2
            stop_loss = round(price - sl_distance, 2)

        tp1 = round(price + (sl_distance * 1.5), 2)
        tp2 = round(price + (sl_distance * 2.5), 2)
        tp3 = round(price + (sl_distance * 4.0), 2)
        swing_tp = round(price + (sl_distance * 6.0), 2)

    elif direction == "SELL":
        best_entry = price
        entry_low = round(price - (atr * 0.1), 2)
        entry_high = round(price + (atr * 0.2), 2)

        stop_loss = round(swing_high + buffer if swing_high else (price + (atr * 1.5)), 2)
        emergency_sl = round(stop_loss + (atr * 0.5), 2)

        sl_distance = stop_loss - price
        if sl_distance <= 0:
            sl_distance = atr * 1.2
            stop_loss = round(price + sl_distance, 2)

        tp1 = round(price - (sl_distance * 1.5), 2)
        tp2 = round(price - (sl_distance * 2.5), 2)
        tp3 = round(price - (sl_distance * 4.0), 2)
        swing_tp = round(price - (sl_distance * 6.0), 2)

    else:
        return {}

    risk_reward = round((tp2 - price) / sl_distance, 2) if direction == "BUY" else round((price - tp2) / sl_distance, 2)

    return {
        'direction': direction,
        'entry_zone_str': f"{entry_low:.2f}–{entry_high:.2f}",
        'entry_low': entry_low,
        'entry_high': entry_high,
        'best_entry': best_entry,
        'stop_loss': stop_loss,
        'emergency_sl': emergency_sl,
        'tp1': tp1,
        'tp2': tp2,
        'tp3': tp3,
        'swing_tp': swing_tp,
        'risk_reward': risk_reward,
        'risk_level': "Medium" if atr < 15.0 else "High"
    }

if __name__ == '__main__':
    plan = generate_trade_plan(3349.10, "BUY", 10.5, 3360.00, 3338.50)
    print("Trade plan generated:", plan)
