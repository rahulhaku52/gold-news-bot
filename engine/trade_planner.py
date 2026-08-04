def generate_trade_plan(price, direction, atr, swing_high, swing_low):
    """
    Generates 100% Dynamic Institutional Trade Plan (v3.5):
    - Primary Plan: Safe Entry, Aggressive Entry, Confirmation Entry, SL, Emergency SL, TP1-3, Swing TP
    - Alternative Scenario Plan: Invalidation trigger, Inverted Entry, Inverted SL, Inverted TP
    """
    if atr is None or atr <= 0:
        atr = 12.0 # Dynamic fallback ATR

    buffer = atr * 0.8

    if direction == "BUY":
        aggressive_entry = price
        safe_entry_low = round(price - (atr * 0.4), 2)
        safe_entry_high = round(price - (atr * 0.1), 2)
        confirmation_entry = round(price + (atr * 0.3), 2)

        stop_loss = round(swing_low - buffer if swing_low else (price - (atr * 1.5)), 2)
        emergency_sl = round(stop_loss - (atr * 0.8), 2)

        sl_distance = price - stop_loss
        if sl_distance <= 0:
            sl_distance = atr * 1.5
            stop_loss = round(price - sl_distance, 2)
            emergency_sl = round(stop_loss - (atr * 0.8), 2)

        tp1 = round(price + (sl_distance * 1.5), 2)
        tp2 = round(price + (sl_distance * 2.5), 2)
        tp3 = round(price + (sl_distance * 4.0), 2)
        swing_tp = round(price + (sl_distance * 6.0), 2)

        # Alternative SELL Plan if SL breaks
        alt_trigger = stop_loss
        alt_entry = round(alt_trigger - (atr * 0.2), 2)
        alt_sl = round(price + (atr * 0.5), 2)
        alt_tp = round(alt_entry - (sl_distance * 2.0), 2)
        alt_plan_str = f"If ${alt_trigger:.2f} breaks on 4H close -> SELL Bias (Entry: ${alt_entry:.2f} | SL: ${alt_sl:.2f} | TP: ${alt_tp:.2f})"

    elif direction == "SELL":
        aggressive_entry = price
        safe_entry_low = round(price + (atr * 0.1), 2)
        safe_entry_high = round(price + (atr * 0.4), 2)
        confirmation_entry = round(price - (atr * 0.3), 2)

        stop_loss = round(swing_high + buffer if swing_high else (price + (atr * 1.5)), 2)
        emergency_sl = round(stop_loss + (atr * 0.8), 2)

        sl_distance = stop_loss - price
        if sl_distance <= 0:
            sl_distance = atr * 1.5
            stop_loss = round(price + sl_distance, 2)
            emergency_sl = round(stop_loss + (atr * 0.8), 2)

        tp1 = round(price - (sl_distance * 1.5), 2)
        tp2 = round(price - (sl_distance * 2.5), 2)
        tp3 = round(price - (sl_distance * 4.0), 2)
        swing_tp = round(price - (sl_distance * 6.0), 2)

        # Alternative BUY Plan if SL breaks
        alt_trigger = stop_loss
        alt_entry = round(alt_trigger + (atr * 0.2), 2)
        alt_sl = round(price - (atr * 0.5), 2)
        alt_tp = round(alt_entry + (sl_distance * 2.0), 2)
        alt_plan_str = f"If ${alt_trigger:.2f} reclaims on 4H close -> BUY Bias (Entry: ${alt_entry:.2f} | SL: ${alt_sl:.2f} | TP: ${alt_tp:.2f})"

    else:
        return {}

    risk_reward = round((tp2 - price) / sl_distance, 2) if direction == "BUY" else round((price - tp2) / sl_distance, 2)

    return {
        'direction': direction,
        'current_price': price,
        'safe_entry_zone': f"{safe_entry_low:.2f}–{safe_entry_high:.2f}",
        'aggressive_entry': aggressive_entry,
        'confirmation_entry': confirmation_entry,
        'stop_loss': stop_loss,
        'emergency_sl': emergency_sl,
        'tp1': tp1,
        'tp2': tp2,
        'tp3': tp3,
        'swing_tp': swing_tp,
        'risk_reward': abs(risk_reward),
        'risk_level': "Medium" if atr < 15.0 else "High",
        'alt_trigger': alt_trigger,
        'alt_plan_str': alt_plan_str
    }

if __name__ == '__main__':
    plan = generate_trade_plan(4098.20, "BUY", 12.5, 4125.00, 4065.00)
    print("Institutional trade plan generated:", plan)
