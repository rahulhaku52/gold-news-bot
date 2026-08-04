import sys
import time
import argparse
from datetime import datetime

import config
from monitor import scheduler

def main():
    parser = argparse.ArgumentParser(description="Gold AI Bot v3 - 22-Layer Institutional Engine")
    parser.add_argument('--scan', action='store_true', help="Run single 22-layer market scan")
    parser.add_argument('--daily-report', action='store_true', help="Generate & post Daily Market Report")
    parser.add_argument('--continuous', action='store_true', help="Run 24/7 continuous monitoring loop")
    parser.add_argument('--test-telegram', action='store_true', help="Send test signal card to Telegram")

    args = parser.parse_args()

    print("==================================================")
    print("🏆 Gold AI Bot v3 - 22-Layer Institutional Engine")
    print("==================================================")

    if args.daily_report:
        print("📊 Running Daily Market Report...")
        scheduler.run_daily_market_report()

    elif args.test_telegram:
        print("🧪 Sending Test Telegram v3 Signal Card...")
        test_plan = {
            'direction': 'BUY',
            'entry_zone_str': '3348.20–3350.00',
            'stop_loss': 3338.50,
            'emergency_sl': 3332.00,
            'tp1': 3362.00,
            'tp2': 3375.00,
            'tp3': 3390.00,
            'swing_tp': 3410.00,
            'risk_level': 'Medium',
            'risk_reward': 2.6
        }
        test_conf = {
            'grade': 'A+',
            'details': {
                'structure': 94,
                'momentum': 90,
                'macro': 89,
                'news': 87,
                'volume': 92,
                'trend': 95,
                'trend_str': 'Bullish',
                'long_term_str': 'Bullish'
            }
        }
        bullets = [
            "Daily trend bullish with confirmed 4H breakout.",
            "Retest of key 3345 Order Block demand level successful.",
            "DXY Dollar Index weakening below 103.80 level.",
            "CPI inflation & dovish Fed expectations supporting Gold.",
            "Volume expansion confirming momentum on lower timeframe."
        ]
        alt_scenario = "<b>Alternative (SELL):</b> Only if $3380 is reclaimed with 4H close & DXY reverses."
        session_info = {'session_name': 'London / New York Overlap (Peak Volatility)'}
        pattern_match_info = {'match_percentage': 97.2, 'recent_cases_str': 'Last 5 Similar Cases: 4 Win, 1 Loss'}
        self_audit_info = {'quality': 'EXCELLENT (A+ APPROVED)'}

        from formatter import telegram_formatter
        card = telegram_formatter.format_trade_signal_card(
            test_plan, test_conf, 93.5, bullets, alt_scenario, 82.4, session_info, pattern_match_info, self_audit_info
        )
        res = scheduler.send_telegram(card)
        print("Telegram test response:", res)

    elif args.continuous:
        print(f"🚀 Starting 24/7 Continuous Scanner (Interval: {config.SCAN_INTERVAL_MINUTES} minutes)...")
        while True:
            try:
                now_utc = datetime.utcnow()
                if now_utc.hour == config.DAILY_REPORT_HOUR_IST and scheduler.LAST_DAILY_REPORT_DATE != now_utc.strftime("%Y-%m-%d"):
                    scheduler.run_daily_market_report()

                scheduler.run_background_scan()
            except Exception as e:
                print(f"❌ Error during scan iteration: {e}")

            time.sleep(config.SCAN_INTERVAL_MINUTES * 60)

    else:
        print("🔍 Executing single 22-layer scan...")
        scheduler.run_background_scan()

if __name__ == '__main__':
    main()
