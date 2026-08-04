def format_progress_bar(score):
    """Renders a progress bar string like '████████ 94'"""
    blocks = int(round(score / 12.5))
    bar = "█" * min(8, max(1, blocks))
    return f"{bar:<8} {int(round(score))}"

def format_trade_signal_card(
    trade_plan,
    confluence_res,
    calibrated_confidence,
    ai_bullets,
    alt_scenario,
    win_rate_stat,
    session_info,
    pattern_match_info,
    self_audit_info
):
    """
    Renders the complete 22-Layer Gold AI Bot v3.5 Telegram Signal Card.
    """
    direction = trade_plan['direction']
    emoji = "🟢" if direction == "BUY" else "🔴"
    grade = confluence_res['grade']
    details = confluence_res['details']

    ai_text = "\n".join([f"• {b.lstrip('•* ')}" for b in ai_bullets])

    msg = f"""━━━━━━━━━━━━━━━━━━━━━━
{emoji} <b>XAU/USD</b>

🔥 <b>{grade} {direction} SETUP</b>
🏛 <i>Session: {session_info.get('session_name', 'London')}</i>

━━━━━━━━━━━━━━━━━━━━━━
📊 <b>Trend & Structure</b>
{details.get('trend_str', 'Bullish')}

━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Entry Zones</b>
• Safe Entry: {trade_plan.get('safe_entry_zone', '')}
• Aggressive Entry: {trade_plan.get('aggressive_entry', 0):.2f}
• Confirmation: {trade_plan.get('confirmation_entry', 0):.2f}

━━━━━━━━━━━━━━━━━━━━━━
🛑 <b>Stop Loss</b>
• SL: {trade_plan['stop_loss']:.2f}
• Emergency SL: {trade_plan['emergency_sl']:.2f}

━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Targets</b>
• TP1: {trade_plan['tp1']:.2f}
• TP2: {trade_plan['tp2']:.2f}
• TP3: {trade_plan['tp3']:.2f}
• Swing TP: {trade_plan['swing_tp']:.2f}

━━━━━━━━━━━━━━━━━━━━━━
🔄 <b>Alternative Scenario</b>
{trade_plan.get('alt_plan_str', '')}

━━━━━━━━━━━━━━━━━━━━━━
📈 <b>Long Term Alignment</b>
{details.get('long_term_str', 'Bullish')}

━━━━━━━━━━━━━━━━━━━━━━
⚠ <b>Risk & R:R</b>
{trade_plan['risk_level']} | Risk:Reward Ratio: 1:{trade_plan['risk_reward']}

━━━━━━━━━━━━━━━━━━━━━━
🧠 <b>AI Analysis</b>
{ai_text}

━━━━━━━━━━━━━━━━━━━━━━
📊 <b>Confluence & Microstructure</b>
Structure  {format_progress_bar(details.get('structure', 90))}
Momentum   {format_progress_bar(details.get('momentum', 90))}
Macro      {format_progress_bar(details.get('macro', 85))}
News       {format_progress_bar(details.get('news', 85))}
Volume     {format_progress_bar(details.get('volume', 90))}
Trend      {format_progress_bar(details.get('trend', 95))}

Confidence Score: {calibrated_confidence}% (Hist. Win Rate: {win_rate_stat}%)
🔍 <b>Pattern Match:</b> {pattern_match_info.get('match_percentage', 96.5)}% ({pattern_match_info.get('recent_cases_str', '')})
🛡 <b>Self-Audit:</b> {self_audit_info.get('quality', 'APPROVED')}

━━━━━━━━━━━━━━━━━━━━━━
🔥 <b>Decision</b>
<b>{direction}</b>
━━━━━━━━━━━━━━━━━━━━━━"""
    return msg

def format_daily_market_report(report_data):
    """Renders the Institutional Grade (v3.5) 60-100 Line Daily Market Report"""
    msg = f"""━━━━━━━━━━━━━━━━━━━━━━
📊 <b>XAU/USD DAILY INSTITUTIONAL REPORT</b>
📅 <i>{report_data.get('date', '')}</i>
━━━━━━━━━━━━━━━━━━━━━━

💰 <b>Current Spot Price:</b> ${report_data.get('current_price', 0):.2f}
📈 <b>Market Regime:</b> {report_data.get('regime', 'Trending')}
🌍 <b>Trading Session:</b> {report_data.get('session', 'London / NY Overlap')}

━━━━━━━━━━━━━━━━━━━━━━
📊 <b>4H Market Structure Analysis</b>
• Structure Bias: <b>{report_data.get('h4_structure', 'BULLISH')}</b>
• Last Structural Event: {report_data.get('h4_event', 'BOS Confirmed')}
• 4H Order Block: {report_data.get('h4_ob', 'Demand Zone Active')}
• Nearest Liquidity Pool: ${report_data.get('h4_liquidity', 0):.2f}
• Zone: {report_data.get('smc_zone', 'Discount')}

━━━━━━━━━━━━━━━━━━━━━━
📊 <b>Daily Market Structure Analysis</b>
• Daily Trend: <b>{report_data.get('daily_trend', 'BULLISH')}</b>
• Structural High/Low: {report_data.get('daily_high_low', 'HH / HL Sequence')}
• Major Resistance: ${report_data.get('r1', 0):.2f}
• Major Support: ${report_data.get('s1', 0):.2f}
• Swing Bias: <b>{report_data.get('bias', 'BULLISH')}</b>

━━━━━━━━━━━━━━━━━━━━━━
🏦 <b>Smart Money Concepts (SMC) & Microstructure</b>
• Liquidity Sweeps: {report_data.get('liquidity_status', 'Equal Lows Swept')}
• Volume Profile / RVOL: {report_data.get('rvol_status', '1.85x (High Vol. Absorption)')}
• Psychology State: {report_data.get('psychology_state', 'Institutional Accumulation')}

━━━━━━━━━━━━━━━━━━━━━━
📈 <b>Technical & Volatility Summary</b>
• EMA Alignment: {report_data.get('ema_status', 'Price > EMA20 > EMA50')}
• RSI (14): {report_data.get('rsi_val', 54.0):.1f} ({report_data.get('rsi_bias', 'Neutral Momentum')})
• ATR Volatility: ${report_data.get('atr_val', 12.5):.2f}

━━━━━━━━━━━━━━━━━━━━━━
🌍 <b>Macro Outlook & News Sentiment</b>
• Macro Backdrop: {report_data.get('macro_summary', 'Fed Rate Cut Expectations / Neutral')}
• Top News Headline: {report_data.get('news_summary', 'Market monitoring economic catalysts.')}
• Intermarket Correlation: {report_data.get('corr_summary', 'DXY Weakness supportive for Gold')}

━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>PRIMARY TRADE PLAN ({report_data.get('primary_direction', 'BUY')})</b>
• Safe Entry Zone: {report_data.get('safe_entry_zone', '')}
• Aggressive Entry: ${report_data.get('aggressive_entry', 0):.2f}
• Confirmation Level: ${report_data.get('confirmation_entry', 0):.2f}
• Stop Loss: ${report_data.get('stop_loss', 0):.2f}
• Emergency SL: ${report_data.get('emergency_sl', 0):.2f}
• TP1: ${report_data.get('tp1', 0):.2f}
• TP2: ${report_data.get('tp2', 0):.2f}
• TP3: ${report_data.get('tp3', 0):.2f}
• Swing TP: ${report_data.get('swing_tp', 0):.2f}

━━━━━━━━━━━━━━━━━━━━━━
🔄 <b>ALTERNATIVE SCENARIO PLAN</b>
{report_data.get('alt_plan_str', 'If Stop Loss breaks on 4H close -> Invert Bias.')}

━━━━━━━━━━━━━━━━━━━━━━
📅 <b>Today's High-Impact Economic Events</b>
{report_data.get('economic_events', '• Clear of immediate high-impact news locks.')}

━━━━━━━━━━━━━━━━━━━━━━
📈 <b>Historical Pattern Similarity & Confluence</b>
• Confluence Score: <b>{report_data.get('confluence_score', 90):.1f}/100</b> ({report_data.get('grade', 'A+')})
• Calibrated Confidence: <b>{report_data.get('calibrated_confidence', 88):.1f}%</b>
• Historical Pattern Match: <b>{report_data.get('pattern_match_pct', 96.5)}%</b> ({report_data.get('pattern_cases_str', '')})

━━━━━━━━━━━━━━━━━━━━━━
🧠 <b>AI Institutional Synthesis</b>
{report_data.get('ai_summary', '• Daily and 4H structure aligned in strong bullish trend.')}

⚠ <i>Educational overview & market breakdown. Risk Level: {report_data.get('risk_level', 'Medium')}. Not financial advice.</i>
━━━━━━━━━━━━━━━━━━━━━━"""
    return msg

def format_trade_update_card(update_info):
    """Renders TP/SL hit updates"""
    utype = update_info['type']
    sig = update_info['signal']
    price = update_info['price']

    if 'TP1' in utype:
        header = "🎯 <b>TP1 HIT!</b>"
        action = "Move Stop Loss to Break-Even (BE)."
    elif 'TP2' in utype:
        header = "🎯 <b>TP2 HIT!</b>"
        action = "Lock in 70% profits."
    elif 'TP3' in utype:
        header = "🎯 <b>TP3 HIT! (Target Accomplished)</b>"
        action = "Full trade closed."
    elif utype == 'SL_HIT':
        header = "🛑 <b>STOP LOSS HIT</b>"
        action = "Trade closed cleanly according to risk plan."
    else:
        header = "ℹ <b>TRADE UPDATE</b>"
        action = "Monitoring continues."

    return f"""━━━━━━━━━━━━━━━━━━━━━━
{header}
📍 <b>Symbol:</b> {sig['symbol']} ({sig['direction']})
💲 <b>Current Price:</b> ${price:.2f}
💡 <b>Action:</b> {action}
━━━━━━━━━━━━━━━━━━━━━━"""

def format_reversal_card(update_info):
    """Renders Reversal / Invalidation alert"""
    sig = update_info['signal']
    reason = update_info['reason']
    watch = update_info['new_watch']

    return f"""━━━━━━━━━━━━━━━━━━━━━━
⚠️ <b>PREVIOUS {sig['direction']} INVALIDATED</b>

<b>Reason:</b>
• {reason}

<b>Status:</b>
{sig['direction']} Closed -> <b>{watch}</b>
━━━━━━━━━━━━━━━━━━━━━━"""

if __name__ == '__main__':
    print("Telegram formatter v3.5 module ready.")
