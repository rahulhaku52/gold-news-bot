# 🏆 Gold AI Bot v3 — 22-Layer Institutional Trading Engine

An enterprise-grade, 22-layer automated market analysis, Smart Money Concepts (SMC), and trade signal engine for **Gold (`XAU/USD`)**, powered by Python, Gemini AI, and GitHub Actions.

---

## 🏛️ 22-Layer Modular Architecture

```
Gold AI Bot v3

├── 1. Multi-Source Data Layer (Yahoo, Metals.live, Finnhub, Stooq, RSS, FRED)
├── 2. Data Validation & Freshness Layer (Timestamp <60s, Spread Mismatch <$1.00)
├── 3. Market Regime Layer (Trending, Ranging, Volatile, News-Driven)
├── 4. Trading Session Engine (LuxAlgo Sessions: London, NY, Tokyo, Sydney, Overlaps)
├── 5. Multi-Timeframe Engine (Monthly, Weekly, Daily, 4H, 1H, 30M, 15M, 5M)
├── 6. Technical Indicator Engine (EMA 20/50/200, VWAP, MACD, RSI, ADX, ATR, Bollinger, Pivots)
├── 7. Advanced Volume Engine (Relative Volume RVOL, Absorption, Climax)
├── 8. Market Structure Engine (LuxAlgo SMC: BOS, CHoCH, Swing HH/HL/LH/LL, EQH/EQL)
├── 9. Smart Money Engine (Bullish & Bearish Order Blocks, Premium/Discount Zones)
├── 10. Price Action Engine (Candlestick Patterns: Engulfing, Pinbar, Doji, Star)
├── 11. Macro Economic Engine (Fed Rates, CPI, NFP, PCE, GDP, PMI, FOMC)
├── 12. Economic News Risk Filter (Pauses signals +/- 15m around high-impact news)
├── 13. Multi-Feed News Engine (RSS Aggregator & Cross-Source Sentiment Verification)
├── 14. Intermarket Correlation Engine (DXY, US10Y Yields, Silver, Oil, SPX, BTC)
├── 15. Market Psychology Engine (Panic, Euphoria, Liquidity Grabs / Stop Hunts)
├── 16. Historical Performance Layer (SQLite Trade & Signal Outcome Tracking)
├── 17. Historical Pattern Matching Layer (Similarity Matrix vs. Past Database Setups)
├── 18. Confidence Calibration Layer (Calibrates score to empirical win rate)
├── 19. Dual AI Reasoning Engine (Gemini AI Primary Plan + Alternative Scenario)
├── 20. Session-Aware Dynamic Confluence Engine (Context-adjusted Score 0-100)
├── 21. Trade Planning & Reversal Engine (Entry Zones, SL, Emergency SL, TP1-3, Reversal Alerts)
└── 22. Pre-Flight Self-Audit Layer (6-Point Safety Checklist before Telegram dispatch)
```

---

## 📁 Repository Structure

```
.
├── config.py                       # Centralized configuration & thresholds
├── requirements.txt                # Dependencies (yfinance, pandas, numpy, scipy, etc.)
├── database/
│   └── performance_db.py           # SQLite database for signal history & win rates
├── data_layer/
│   ├── multi_source.py             # Multi-provider price & candle data fetcher
│   └── validator.py                # Freshness check (<60s) & price spread validator
├── engine/
│   ├── regime_engine.py            # Session & Regime-aware dynamic weight adjustments
│   ├── session_engine.py           # LuxAlgo PineScript Sessions translated to Python
│   ├── timeframe_engine.py         # Multi-timeframe trend alignment matrix
│   ├── technical_engine.py         # EMA, MACD, RSI, ATR, Bollinger, Pivots
│   ├── volume_engine.py            # Relative Volume (RVOL) & Volume Absorption
│   ├── market_structure.py         # LuxAlgo SMC: Swing points, BOS, CHoCH, EQH/EQL
│   ├── smart_money.py              # Order Blocks (OB) & Premium/Discount Zones
│   ├── price_action.py             # Candlestick pattern detection
│   ├── macro_engine.py             # Macro economic release evaluator
│   ├── news_risk_filter.py         # Safety window filter around high-impact news
│   ├── news_engine.py              # RSS multi-feed parsing & sentiment scoring
│   ├── correlation_engine.py       # DXY, US10Y, Silver, Oil correlation engine
│   ├── market_psychology.py        # Stop Hunts, Liquidity Grabs, Exhaustion
│   ├── performance_layer.py        # Historical signal lookup & win rate stats
│   ├── pattern_matcher.py          # Setup pattern similarity matching
│   ├── confidence_calibrator.py    # Win rate score calibration
│   ├── ai_reasoning.py             # Gemini AI Dual-Scenario generator
│   ├── confluence_engine.py        # Weighted score calculator (0-100)
│   ├── trade_planner.py            # Entry zones, SL, TPs, R:R calculation
│   ├── reversal_detector.py        # Active trade tracking & CHoCH reversal alerts
│   └── signal_auditor.py           # Pre-flight self-audit checklist
├── monitor/
│   └── scheduler.py                # 24/7 Background scanner & Daily 08:00 AM IST Report
├── formatter/
│   └── telegram_formatter.py       # HTML template formatter for Telegram cards
├── main.py                         # CLI application entrypoint
└── .github/workflows/
    └── gold_bot_v2.yml             # GitHub Actions workflow for automated 24/7 runs
```

---

## ⚡ Setup & Deployment Guide

### Option 1: GitHub Actions Deployment (Recommended)
1. Fork or push this repository to GitHub.
2. Go to **Settings > Secrets and variables > Actions** and add the following repository secrets:
   - `BOT_TOKEN`: Your Telegram Bot Token.
   - `CHANNEL_ID`: Your Telegram Channel ID (e.g. `@yourchannel`).
   - `GEMINI_API_KEY`: Your Gemini API Key.
   - `FINNHUB_KEY` *(Optional)*: Free Finnhub API Key for data redundancy.
3. GitHub Actions will automatically execute the **Daily Market Report every day at 08:00 AM IST** and run background scans every 15 minutes!

### Option 2: Local Server Execution
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gold-ai-bot.cmd
   cd gold-ai-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables in `.env` or system environment:
   ```env
   BOT_TOKEN="your_bot_token"
   CHANNEL_ID="your_channel_id"
   GEMINI_API_KEY="your_gemini_key"
   ```
4. Run a single scan or start the continuous loop:
   ```bash
   # Execute single scan
   python main.py --scan

   # Generate Daily Market Report
   python main.py --daily-report

   # Start 24/7 continuous scanner
   python main.py --continuous
   ```

---

## 🛡️ License

This project is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License.
