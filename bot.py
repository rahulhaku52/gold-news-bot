import os, requests, feedparser, json, re, subprocess

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

RSS_FEED = "https://www.investing.com/rss/news_gold.rss"
LOG_FILE = "posted_articles.json"

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

def build_message(title, summary):
    return (
        f"📰 <b>Gold Market Update</b>\n\n"
        f"🔹 <b>{title}</b>\n\n"
        f"📝 {summary[:300]}...\n\n"
        f"<i>Source: Investing.com</i>\n"
        f"#XAUUSD #GoldNews"
    )

def fetch_new(posted_ids):
    feed = feedparser.parse(RSS_FEED)
    for entry in feed.entries:
        article_id = entry.get('id') or entry.get('link')
        if article_id not in posted_ids:
            title = entry.title
            summary = entry.summary if hasattr(entry, 'summary') else ""
            msg = build_message(title, clean_html(summary))
            return article_id, msg
    return None, None

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
            print("ℹ️  No change.")
    except Exception as e:
        print(f"⚠️  Git error: {e}")

def main():
    posted = load_posted()
    article_id, msg = fetch_new(posted)
    if msg:
        res = send_to_telegram(msg)
        if res.get('ok'):
            posted.add(article_id)
            save_posted(posted)
            print("✅ Gold news posted:", article_id)
            git_commit_log()
        else:
            print("❌ API error:", res)
    else:
        print("ℹ️  No new gold news.")

if __name__ == "__main__":
    main()
