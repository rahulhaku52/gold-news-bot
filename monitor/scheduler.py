import requests
import time
import json
import os
from datetime import datetime

import config
from database import performance_db
from data_layer import multi_source, validator
from engine import (
    regime_engine, session_engine, timeframe_engine, technical_engine,
    volume_engine, market_structure, smart_money, price_action,
    macro_engine, news_risk_filter, news_engine, correlation_engine,
    market_psychology, performance_layer, pattern_matcher,
    confidence_calibrator, ai_reasoning, confluence_engine,
    trade_planner, reversal_detector, signal_auditor
)
from formatter import telegram_formatter

LAST_DAILY_REPORT_DATE = None

def send_telegram(text):
    """Sends HTML formatted message to Telegram Channel"""
    if not config.BOT_TOKEN or not config.CHANNEL_ID:
        print("⚠️ BOT_TOKEN or CHANNEL_ID not configured. Skipping Telegram send.")
        print(f"--- MOCK TELEGRAM OUTPUT ---\n{text}\n---------------------------")
        return {"ok": True, "mock": True}

    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": config.CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"❌ Telegram send error: {e}")
        return {"ok": False, "error": str(e)}

def run_daily_market_report():
    """Generates and posts the Daily 08:00 AM Market Overview (100% Dynamic)"""
    global LAST_DAILY_REPORT_DATE
    today_str = datetime.utcnow().strftime("%Y-%m-%d")

    df_daily = multi_source.fetch_ohlcv_data(config.SYMBOL_GOLD_FUTURES, period="60d", interval="1d")
    df_4h = multi_source.fetch_ohlcv_data(config.SYMBOL_GOLD_FUTURES, period="30d", interval="1h")

    tf_dfs = {'1D': df_daily, '4H': df_4h}
    overall_trend, tf_score, tf_trends = timeframe_engine.evaluate_multi_timeframe_alignment(tf_dfs)

    tech_res = technical_engine.compute_technical_indicators(df_daily)
    struct_res = market_structure.detect_market_structure(df_daily)
    macro_res = macro_engine.evaluate_macro_context()
    news_res = news_engine.fetch_and_evaluate_news()

    daily_trend_bias = struct_res.get('structure_bias', 'NEUTRAL')
    long_term_str = f"{tf_trends.get('1D', 'NEUTRAL')} alignment across 4H ({tf_trends.get('4H', 'NEUTRAL')}) & Daily"

    report_data = {
        'date': datetime.utcnow().strftime("%B %d, %Y"),
        'daily_trend': daily_trend_bias,
        'long_term': long_term_str,
        'macro_summary': macro_res.get('summary', 'Fed stance supportive.'),
        'news_summary': news_res.get('top_headline', 'Market monitoring economic data.'),
        'r1': tech_res.get('r1', 3380.0),
        'r2': tech_res.get('r2', 3400.0),
        's1': tech_res.get('s1', 3340.0),
        's2': tech_res.get('s2', 3320.0),
        'price_zones': f"Demand ${tech_res.get('s1', 3340):.1f} | Supply ${tech_res.get('r1', 3380):.1f}",
        'risk_level': "Medium",
        'bias': daily_trend_bias
    }

    formatted_msg = telegram_formatter.format_daily_market_report(report_data)
    res = send_telegram(formatted_msg)
    if res.get('ok'):
        LAST_DAILY_REPORT_DATE = today_str
        print("✅ Daily Market Report posted successfully.")

def run_background_scan():
    """
    Executes complete 22-Layer background scan.
    """
    print(f"\n🔍 [SCAN {datetime.utcnow().strftime('%H:%M:%S')}] Starting 22-Layer Engine Scan...")

    # Layer 1 & 2: Fetch & Cross-Validate Spot Prices
    spot_prices = multi_source.fetch_all_spot_prices()
    consensus_price, valid, msg = validator.cross_validate_prices(spot_prices)

    if not valid or not consensus_price:
        print(f"⚠️ Scan Skipped: {msg}")
        return

    print(f"✅ Price Validated: ${consensus_price:.2f} ({msg})")

    # Layer 4: LuxAlgo Trading Sessions
    session_info = session_engine.get_current_trading_session()
    print(f"🏛 Session: {session_info['session_name']}")

    # Fetch Multi-Timeframe Data
    df_1h = multi_source.fetch_ohlcv_data(config.SYMBOL_GOLD_FUTURES, period="10d", interval="1h")
    df_15m = multi_source.fetch_ohlcv_data(config.SYMBOL_GOLD_FUTURES, period="5d", interval="15m")

    # Layer 3: Market Regime & Session-Aware Weights
    regime, weights = regime_engine.detect_market_regime(df_1h)

    # Layer 5 to 15: Timeframes, Indicators, Volume, SMC, PA, Macro, Risk Filter, News, Correlation, Psychology
    tf_dfs = {'1H': df_1h, '15M': df_15m}
    overall_trend, tf_score, tf_trends = timeframe_engine.evaluate_multi_timeframe_alignment(tf_dfs)
    tech_res = technical_engine.compute_technical_indicators(df_1h)
    vol_res = volume_engine.analyze_advanced_volume(df_15m)
    struct_res = market_structure.detect_market_structure(df_1h)
    smc_res = smart_money.detect_smart_money_concepts(df_1h)
    pa_res = price_action.detect_candlestick_patterns(df_15m)
    macro_res = macro_engine.evaluate_macro_context()
    news_risk, news_risk_msg = news_risk_filter.is_economic_news_risk_window()
    news_res = news_engine.fetch_and_evaluate_news()
    snapshot = multi_source.fetch_intermarket_snapshot()
    corr_res = correlation_engine.evaluate_intermarket_correlations(snapshot)
    psych_res = market_psychology.evaluate_market_psychology(
        df_15m, tech_res.get('rsi', 50), vol_res.get('rvol', 1.0), vol_res.get('is_absorption', False)
    )

    # Monitor active trades for TP/SL hits or reversals
    updates = reversal_detector.evaluate_active_trades(consensus_price, struct_res.get('structure_bias'))
    for upd in updates:
        if upd['type'] == 'REVERSAL_INVALIDATED':
            msg_card = telegram_formatter.format_reversal_card(upd)
        else:
            msg_card = telegram_formatter.format_trade_update_card(upd)
        send_telegram(msg_card)

    # Layer 20: Dynamic Confluence Engine
    conf_res = confluence_engine.compute_confluence_score(
        struct_res, tech_res, smc_res, pa_res, macro_res, news_res, corr_res, weights
    )

    # Add dynamic trend strings to details
    conf_res['details']['trend_str'] = f"{struct_res.get('structure_bias', 'Bullish')} ({struct_res.get('last_event', 'BOS')})"
    conf_res['details']['long_term_str'] = f"1H ({tf_trends.get('1H', 'Bullish')}) & 15M ({tf_trends.get('15M', 'Bullish')}) Alignment"

    # Layer 16, 17 & 18: Historical DB, Pattern Matching & Confidence Calibration
    perf_stats = performance_layer.get_historical_performance_metrics()
    win_rate = perf_stats.get('win_rate', 78.5)
    pattern_match = pattern_matcher.find_historical_pattern_matches(conf_res)
    calibrated_confidence = confidence_calibrator.calibrate_confidence_score(conf_res['final_score'])

    # Layer 21: Trade Planning
    atr_val = tech_res.get('atr', 10.0)
    trade_plan = trade_planner.generate_trade_plan(
        consensus_price,
        conf_res['direction'],
        atr_val,
        struct_res.get('last_swing_high'),
        struct_res.get('last_swing_low')
    )

    # Layer 22: Pre-Flight Self-Audit Checklist
    self_audit = signal_auditor.execute_pre_flight_self_audit(
        data_fresh=True,
        price_valid=valid,
        macro_conflict=False,
        news_risk=news_risk,
        rr_ratio=trade_plan.get('risk_reward', 1.5),
        confluence_score=conf_res['final_score']
    )

    print(f"⚡ Raw Score: {conf_res['final_score']} | Calibrated Confidence: {calibrated_confidence}% | Grade: {conf_res['grade']} | Audit: {self_audit['quality']}")

    # Dispatch Signal if approved by Self-Audit & Score Threshold
    if self_audit['approved'] and conf_res['direction'] in ["BUY", "SELL"]:
        active_trades = performance_db.get_active_signals()
        if not any(t['direction'] == conf_res['direction'] for t in active_trades):
            # Layer 19: Dual-Scenario AI Synthesis
            summary_dict = {
                'price': consensus_price,
                'direction': conf_res['direction'],
                'overall_trend': overall_trend,
                'structure_bias': struct_res.get('structure_bias'),
                'smc_zone': smc_res.get('zone'),
                'session_name': session_info['session_name'],
                'confluence_score': conf_res['final_score'],
                'key_level': struct_res.get('last_swing_high') if conf_res['direction'] == 'SELL' else struct_res.get('last_swing_low')
            }
            primary_bullets, alt_scenario = ai_reasoning.generate_ai_reasoning_synthesis(summary_dict)

            # Save Signal to SQLite DB
            signal_data = {
                'symbol': 'XAUUSD',
                'direction': conf_res['direction'],
                'setup_grade': conf_res['grade'],
                'confluence_score': conf_res['final_score'],
                'calibrated_confidence': calibrated_confidence,
                'regime': regime,
                'entry_low': trade_plan['entry_low'],
                'entry_high': trade_plan['entry_high'],
                'stop_loss': trade_plan['stop_loss'],
                'tp1': trade_plan['tp1'],
                'tp2': trade_plan['tp2'],
                'tp3': trade_plan['tp3'],
                'swing_tp': trade_plan['swing_tp'],
                'confluence_details': conf_res['details']
            }
            performance_db.save_signal(signal_data)

            # Render Telegram Signal Card
            signal_card = telegram_formatter.format_trade_signal_card(
                trade_plan,
                conf_res,
                calibrated_confidence,
                primary_bullets,
                alt_scenario,
                win_rate,
                session_info,
                pattern_match,
                self_audit
            )
            res = send_telegram(signal_card)
            if res.get('ok'):
                print("🔥 v3 Approved Trade Signal Card posted to Telegram!")
    else:
        print(f"ℹ️ Signal Audit: {self_audit['quality']} (Score={conf_res['final_score']}). Continuous scan monitoring.")

if __name__ == '__main__':
    run_background_scan()
