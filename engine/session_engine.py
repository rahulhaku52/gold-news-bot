from datetime import datetime

def get_current_trading_session(utc_dt=None):
    """
    LuxAlgo Sessions Python Translation:
    - Tokyo / Asian: 00:00 - 09:00 UTC
    - London: 07:00 - 16:00 UTC
    - New York: 13:00 - 22:00 UTC
    - Sydney: 21:00 - 06:00 UTC
    Detects active sessions and high-volatility overlaps (London / NY Overlap: 13:00 - 16:00 UTC).
    """
    if utc_dt is None:
        utc_dt = datetime.utcnow()

    hour = utc_dt.hour

    active_sessions = []
    if 0 <= hour < 9:
        active_sessions.append("Tokyo")
    if 7 <= hour < 16:
        active_sessions.append("London")
    if 13 <= hour < 22:
        active_sessions.append("New York")
    if hour >= 21 or hour < 6:
        active_sessions.append("Sydney")

    is_overlap = ("London" in active_sessions and "New York" in active_sessions)

    if is_overlap:
        session_name = "London / New York Overlap (Peak Volatility)"
        volatility_multiplier = 1.3
    elif "New York" in active_sessions:
        session_name = "New York Session (High Volatility)"
        volatility_multiplier = 1.2
    elif "London" in active_sessions:
        session_name = "London Session (Medium-High Volatility)"
        volatility_multiplier = 1.15
    elif "Tokyo" in active_sessions:
        session_name = "Tokyo / Asian Session (Consolidation / Range)"
        volatility_multiplier = 0.85
    else:
        session_name = "Sydney / Asian Session (Low Volatility)"
        volatility_multiplier = 0.75

    return {
        'active_sessions': active_sessions,
        'session_name': session_name,
        'is_overlap': is_overlap,
        'volatility_multiplier': volatility_multiplier
    }

if __name__ == '__main__':
    print("Session engine test:", get_current_trading_session())
