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
    Renders the complete 22-Layer Gold AI Bot v3 Telegram Signal Card.
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
📊 <b>Trend</b>
{details.get('trend_str', 'Bullish')}

━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Entry</b>
{trade_plan['entry_zone_str']}

━━━━━━━━━━━━━━━━━━━━━━
🛑 <b>Stop Loss</b>
{trade_plan['stop_loss']:.2f} (Emergency SL: {trade_plan['emergency_sl']:.2f})

━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Targets</b>
• TP1: {trade_plan['tp1']:.2f}
• TP2: {trade_plan['tp2']:.2f}
• TP3: {trade_plan['tp3']:.2f}
• Swing TP: {trade_plan['swing_tp']:.2f}

━━━━━━━━━━━━━━━━━━━━━━
📈 <b>Long Term</b>
{details.get('long_term_str', 'Bullish')}

━━━━━━━━━━━━━━━━━━━━━━
⚠ <b>Risk & R:R</b>
{trade_plan['risk_level']} | R:R Ratio: 1:{trade_plan['risk_reward']}

━━━━━━━━━━━━━━━━━━━━━━
🧠 <b>AI Analysis (Primary Plan)</b>
{ai_text}

⚡ {alt_scenario}

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
    """Renders the Daily 08:00 AM IST Market Overview"""
    msg = f"""📊 <b>GOLD (XAUUSD) DAILY MARKET REPORT</b>
📅 {report_data.get('date', '')}

━━━━━━━━━━━━━━━━━━━━━━
📈 <b>Daily Trend:</b> {report_data.get('daily_trend', 'Bullish')}
📊 <b>Long-Term (4H/1D):</b> {report_data.get('long_term', 'Bullish')}
🌍 <b>Macro Outlook:</b> {report_data.get('macro_summary', 'Fed Dovish / Neutral')}
📰 <b>News Summary:</b> {report_data.get('news_summary', 'Market watching inflation metrics.')}

🎯 <b>Key S&R Levels:</b>
• Resistance 2: ${report_data.get('r2', 0):.2f}
• Resistance 1: ${report_data.get('r1', 0):.2f}
• Support 1: ${report_data.get('s1', 0):.2f}
• Support 2: ${report_data.get('s2', 0):.2f}

🎯 <b>Important Price Zones:</b> {report_data.get('price_zones', 'Demand 3340-3345 | Supply 3380-3385')}
⚠ <b>Risk Level:</b> {report_data.get('risk_level', 'Medium')}
🧠 <b>Overall Market Bias:</b> {report_data.get('bias', 'BULLISH')}

<i>Educational overview. Not financial advice.</i>
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
    print("Telegram formatter v3 module ready.")
