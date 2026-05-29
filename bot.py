import os, requests, feedparser, json, re, subprocess, time

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

# ========== RSS ফিড লিস্ট (নতুন ফিড সহজেই যোগ করা যাবে) ==========
RSS_FEEDS = [
    # গোল্ড
    "https://www.investing.com/rss/news_gold.rss",
    # ক্রিপ্টো
    "https://www.investing.com/rss/news_cryptocurrency.rss",
    # অয়েল (ক্রুড অয়েল)
    "https://www.investing.com/rss/news_commodities_crude_oil.rss",
    # সাধারণ ফিন্যান্সিয়াল নিউজ
    "https://www.marketwatch.com/feeds/marketwatch/bulletins",  # MarketWatch
    "https://feeds.feedburner.com/CoinDesk",                     # CoinDesk (ক্রিপ্টো)
]

LOG_FILE = "posted_articles.json"
MAX_POSTS_PER_RUN = 5   # এক রানে সর্বোচ্চ কয়টা পোস্ট করবে

def load_posted():
    try:
        with open(LOG_FILE, 'r') as f:
            return set(json.load(f))
    except:
        return set()

def save_posted(posted):
    with open(LOG_FILE, 'w') as f:
        json.dump(list(posted), f)

def clean_html(raw):
    return re.sub(r'<[^>]+>', '', raw).strip()

def build_message(feed_name, title, summary):
    """প্রতিটি ফিডের জন্য আলাদা হেডার ও হ্যাশট্যাগ"""
    if "gold" in feed_name.lower():
        header = "📰 Gold Market Update"
        tags = "#XAUUSD #GoldNews"
    elif "cryptocurrency" in feed_name.lower() or "coindesk" in feed_name.lower():
        header = "₿ Crypto Update"
        tags = "#Crypto #Bitcoin"
    elif "crude_oil" in feed_name.lower():
        header = "🛢 Crude Oil Update"
        tags = "#Oil #WTI"
    else:
        header = "📊 Market News"
        tags = "#MarketNews #Forex"

    return (
        f"{header}\n\n"
        f"🔹 <b>{title}</b>\n\n"
        f"📝 {summary[:300]}...\n\n"
        f"<i>Source: {feed_name}</i>\n"
        f"{tags}"
    )

def fetch_all_new(posted_ids):
    """সব ফিড থেকে নতুন আর্টিকেল সংগ্রহ করবে, সর্বোচ্চ MAX_POSTS_PER_RUN টা নেবে"""
    new_articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            feed_name = feed.feed.title if 'title' in feed.feed else feed_url
            for entry in feed.entries:
                article_id = entry.get('id') or entry.get('link')
                if article_id not in posted_ids:
                    title = entry.title
                    summary = entry.summary if hasattr(entry, 'summary') else ""
                    clean_summary = clean_html(summary)
                    msg = build_message(feed_name, title, clean_summary)
                    new_articles.append((article_id, msg))
                    if len(new_articles) >= MAX_POSTS_PER_RUN:
                        break
        except Exception as e:
            print(f"⚠️ Error parsing {feed_url}: {e}")
        if len(new_articles) >= MAX_POSTS_PER_RUN:
            break
    return new_articles

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    return requests.post(url, json={
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }).json()

def git_commit_log():
    try:
        subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)
        subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "add", LOG_FILE], check=True)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
        if diff.returncode != 0:
            subprocess.run(["git", "commit", "-m", "Update posted log"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("✅ Log committed.")
        else:
            print("ℹ️  No change in log.")
    except Exception as e:
        print(f"⚠️  Git commit error: {e}")

def main():
    print("🔍 Checking multiple RSS feeds...")
    posted = load_posted()
    new_articles = fetch_all_new(posted)

    if new_articles:
        print(f"Found {len(new_articles)} new articles. Posting...")
        for article_id, msg in new_articles:
            res = send_to_telegram(msg)
            if res.get('ok'):
                posted.add(article_id)
                print(f"✅ Posted: {article_id[:50]}...")
                time.sleep(1)  # রেট লিমিট এড়াতে একটু বিরতি
            else:
                print(f"❌ Failed to post: {res}")
        save_posted(posted)
        git_commit_log()
    else:
        print("ℹ️  No new articles across all feeds. Skipping.")

if __name__ == "__main__":
    main()
