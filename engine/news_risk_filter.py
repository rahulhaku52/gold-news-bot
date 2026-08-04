from datetime import datetime

HIGH_IMPACT_EVENTS = ["CPI", "NFP", "FOMC", "Fed Interest Rate", "PCE Inflation", "GDP"]

def is_economic_news_risk_window(upcoming_events=None):
    """
    Checks if current time is within +/- 15 minutes of high-impact economic news releases.
    If true, signal generation is paused to avoid slippage and market noise.
    """
    if not upcoming_events:
        return False, "Clear of high-impact news windows."

    now = datetime.utcnow()
    for event in upcoming_events:
        event_name = event.get('name', '')
        event_time = event.get('time') # datetime object
        if any(h in event_name for h in HIGH_IMPACT_EVENTS) and event_time:
            time_diff_mins = abs((now - event_time).total_seconds()) / 60.0
            if time_diff_mins <= 15.0:
                return True, f"High-impact event '{event_name}' scheduled within {int(time_diff_mins)} minutes. Pausing new signal alerts."

    return False, "Clear of high-impact news windows."

if __name__ == '__main__':
    print("News risk filter module ready.")
