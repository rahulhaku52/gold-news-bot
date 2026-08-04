import pandas as pd
import numpy as np
from engine import session_engine

def detect_market_regime(df_1h, news_active=False):
    """
    Session & Regime-Aware Dynamic Weight Adjustment:
    Combines Market Regime (Trending, Ranging, Volatile, News-Driven) with Active Trading Session (London/NY Overlap, Tokyo).
    """
    session_info = session_engine.get_current_trading_session()
    is_overlap = session_info.get('is_overlap', False)

    if df_1h is None or df_1h.empty or len(df_1h) < 50:
        regime = 'Trending'
    else:
        close = df_1h['Close']
        high = df_1h['High']
        low = df_1h['Low']

        # ATR Ratio
        tr = np.maximum(high - low, np.maximum(abs(high - close.shift(1)), abs(low - close.shift(1))))
        atr20 = tr.rolling(20).mean().iloc[-1]
        atr100 = tr.rolling(100).mean().iloc[-1]

        # Price Range Efficiency Ratio
        price_range = high.rolling(14).max() - low.rolling(14).min()
        body_move = abs(close - close.shift(14))
        efficiency_ratio = (body_move / price_range).iloc[-1] if not price_range.empty and price_range.iloc[-1] > 0 else 0.5

        if news_active:
            regime = 'News-Driven'
        elif atr100 > 0 and (atr20 / atr100) > 1.7:
            regime = 'High Volatility'
        elif efficiency_ratio < 0.35:
            regime = 'Ranging'
        else:
            regime = 'Trending'

    # Dynamic Weight Allocation Matrix
    if regime == 'News-Driven':
        weights = {
            'market_structure': 20,
            'macro': 35,
            'momentum_technical': 10,
            'price_action': 15,
            'correlation': 10,
            'news': 5,
            'risk_volatility': 5
        }
    elif is_overlap:
        # London / NY Overlap: Institutional Order Flow & SMC structure takes priority
        weights = {
            'market_structure': 40,
            'macro': 15,
            'momentum_technical': 15,
            'price_action': 15,
            'correlation': 5,
            'news': 5,
            'risk_volatility': 5
        }
    elif regime == 'Ranging' or "Tokyo" in session_info.get('active_sessions', []):
        # Ranging / Asian session: Mean reversion & Oscillators (RSI/Bollinger) take priority
        weights = {
            'market_structure': 20,
            'macro': 10,
            'momentum_technical': 30,
            'price_action': 25,
            'correlation': 5,
            'news': 5,
            'risk_volatility': 5
        }
    elif regime == 'High Volatility':
        weights = {
            'market_structure': 25,
            'macro': 15,
            'momentum_technical': 15,
            'price_action': 15,
            'correlation': 10,
            'news': 10,
            'risk_volatility': 10
        }
    else: # Default Trending
        weights = {
            'market_structure': 35,
            'macro': 15,
            'momentum_technical': 15,
            'price_action': 15,
            'correlation': 10,
            'news': 5,
            'risk_volatility': 5
        }

    return regime, weights

if __name__ == '__main__':
    print("Session & Regime aware engine test:", detect_market_regime(None))
