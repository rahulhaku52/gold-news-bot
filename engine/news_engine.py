import feedparser
import re
import config

IMPORTANT_KEYWORDS = [
    "gold", "xauusd", "xau", "silver", "crude oil", "wti", "brent",
    "fed", "federal reserve", "ecb", "central bank", "interest rate",
    "inflation", "cpi", "gdp", "nfp", "fomc", "rally", "bull", "bear",
    "war", "geopolitical", "yields", "dollar", "dxy"
]

def clean_html(raw_html):
    return re.sub(r'<[^>]+>', '', raw_html).strip()

def analyze_news_sentiment(text):
    text_lower = text.lower()
    bullish_terms = ["surge", "rally", "gain", "bull", "record high", "cut rate", "safe haven", "breakout"]
    bearish_terms = ["drop", "fall", "plunge", "bear", "hike rate", "strong dollar", "dump", "selloff"]

    bull_count = sum(1 for term in bullish_terms if term in text_lower)
    bear_count = sum(1 for term in bearish_terms if term in text_lower)

    if bull_count > bear_count:
        return "BULLISH"
    elif bear_count > bull_count:
        return "BEARISH"
    else:
        return "NEUTRAL"

def fetch_and_evaluate_news():
    """
    Parses RSS feeds, verifies important headlines across multiple sources,
    and returns sentiment score (0 - 100) and top headline.
    """
    articles = []
    bullish_articles = 0
    bearish_articles = 0

    for feed_url in config.RSS_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[:5]:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                combined = (title + " " + summary).lower()
                if any(kw in combined for kw in IMPORTANT_KEYWORDS):
                    sent = analyze_news_sentiment(combined)
                    articles.append({'title': title, 'sentiment': sent})
                    if sent == "BULLISH":
                        bullish_articles += 1
                    elif sent == "BEARISH":
                        bearish_articles += 1
        except Exception as e:
            print(f"⚠️ RSS parse error for {feed_url}: {e}")

    total = len(articles)
    if total == 0:
        return {'news_score': 50.0, 'sentiment': 'NEUTRAL', 'top_headline': 'No major news breaking.'}

    if bullish_articles > bearish_articles:
        sentiment = "BULLISH"
        score = 70.0 + min(20.0, (bullish_articles / total) * 30.0)
    elif bearish_articles > bullish_articles:
        sentiment = "BEARISH"
        score = 30.0 - min(20.0, (bearish_articles / total) * 30.0)
    else:
        sentiment = "NEUTRAL"
        score = 50.0

    top_title = articles[0]['title'] if articles else "Market watching macro catalysts."

    return {
        'news_score': score,
        'sentiment': sentiment,
        'articles_count': total,
        'top_headline': top_title
    }

if __name__ == '__main__':
    print("Testing news engine...")
    print(fetch_and_evaluate_news())
