import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Environment Credentials (support multiple common secret names)
BOT_TOKEN = os.environ.get('BOT_TOKEN') or os.environ.get('TELEGRAM_BOT_TOKEN', '')
CHANNEL_ID = os.environ.get('CHANNEL_ID') or os.environ.get('TELEGRAM_CHAT_ID') or os.environ.get('TELEGRAM_CHANNEL_ID', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY', '')
FINNHUB_KEY = os.environ.get('FINNHUB_KEY', '')
ALPHA_VANTAGE_KEY = os.environ.get('ALPHA_VANTAGE_KEY', '')

# Gemini Model Config
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash')

# Primary Tickers (Spot Gold XAUUSD focus - DO NOT USE Futures GC=F for Spot)
SYMBOL_GOLD_SPOT = "XAUUSD=X"
SYMBOL_GOLD_FUTURES = "XAUUSD=X" # Primary spot ticker on Yahoo Finance
SYMBOL_SILVER = "SI=F"
SYMBOL_OIL = "CL=F"
SYMBOL_DXY_TICKERS = ["UUP", "DX=F"]
SYMBOL_DXY = "UUP"
SYMBOL_US10Y = "^TNX"
SYMBOL_US2Y = "^IRX"
SYMBOL_SPX = "^GSPC"
SYMBOL_NASDAQ = "^IXIC"
SYMBOL_BTC = "BTC-USD"
SYMBOL_USDJPY = "USDJPY=X"
SYMBOL_EURUSD = "EURUSD=X"

# Thresholds & Limits
MAX_DATA_AGE_SECONDS = 60
MAX_PRICE_MISMATCH_DOLLARS = 1.50 # Max allowed spread across spot sources

# Timeframes
TIMEFRAMES = ["M", "W", "D", "4H", "1H", "30M", "15M", "5M"]

# Default Confluence Weights (%)
DEFAULT_WEIGHTS = {
    "market_structure": 25,
    "macro": 20,
    "momentum_technical": 15,
    "price_action": 15,
    "correlation": 10,
    "news": 10,
    "risk_volatility": 5
}

# Telegram Posting Thresholds
MIN_CONFLUENCE_FOR_SIGNAL = 85.0 # A/A+ Setup
DAILY_REPORT_HOUR_IST = 8 # 08:00 AM IST
SCAN_INTERVAL_MINUTES = 5

# Database Path
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "signals.db")
LOG_FILE = os.path.join(os.path.dirname(__file__), "posted_articles.json")

# RSS Feeds
RSS_FEEDS = [
    "https://www.investing.com/rss/news_gold.rss",
    "https://www.investing.com/rss/news_cryptocurrency.rss",
    "https://www.investing.com/rss/news_commodities_crude_oil.rss",
    "https://www.marketwatch.com/feeds/marketwatch/bulletins",
    "https://feeds.feedburner.com/CoinDesk",
]
