import os, requests, json
import yfinance as yf
import pandas as pd
import numpy as np
import google.generativeai as genai

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

def fetch_gold_data():
    gold = yf.Ticker("GC=F")
    hist = gold.history(period="30d", interval="1h")
    return hist

def compute_indicators(df):
    if df.empty:
        return None
    close = df['Close']
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    current_rsi = rsi.iloc[-1]
    sma20 = close.rolling(window=20).mean().iloc[-1]
    sma50 = close.rolling(window=50).mean().iloc[-1]
    current_price = close.iloc[-1]
    prev_close = close.iloc[-2] if len(close) > 1 else current_price
    change_pct = ((current_price - prev_close) / prev_close) * 100
    return {
        "price": current_price,
        "change_pct": change_pct,
        "rsi": current_rsi,
        "sma20": sma20,
        "sma50": sma50
    }

def generate_ai_analysis(data):
    if not data:
        return "XAUUSD data unavailable at this moment."
    prompt = f"""
You are a professional financial market educator. Based on the following XAUUSD (gold) technical indicators, write a concise, educational analysis in standard English. Do NOT give any buy/sell trading signals. Explain what the indicators suggest about current market conditions in a neutral, informative tone. Keep it under 300 words.

Current price: ${data['price']:.2f}
Change: {data['change_pct']:+.2f}%
RSI (14): {data['rsi']:.1f}
SMA 20: ${data['sma20']:.2f}
SMA 50: ${data['sma50']:.2f}

Explain the meaning of RSI level (overbought/oversold/neutral), the relation between SMA20 and SMA50 (trend), and overall technical context. Mention that this is for educational purposes only, not financial advice.
"""
    try:
        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        # ক্লিন Markdown বোল্ড → HTML
        ai_text = ai_text.replace("**", "<b>").replace("**", "</b>")
        return (
            f"📊 <b>XAUUSD Technical Overview (AI-Enhanced)</b>\n\n"
            f"{ai_text}\n\n"
            f"<i>Data: Yahoo Finance | Powered by Gemini AI | Educational purpose only</i>\n"
            f"#XAUUSD #GoldAnalysis #Educational"
        )
    except Exception as e:
        print(f"⚠️ Gemini error: {e}")
        return None

def generate_simple_analysis(data):
    if not data:
        return "XAUUSD data unavailable."
    price = data['price']
    rsi = data['rsi']
    sma20 = data['sma20']
    sma50 = data['sma50']
    change = data['change_pct']
    rsi_comment = ""
    if rsi > 70:
        rsi_comment = f"RSI at {rsi:.1f} – Overbought territory. A pullback may occur."
    elif rsi < 30:
        rsi_comment = f"RSI at {rsi:.1f} – Oversold territory. A bounce is possible."
    else:
        rsi_comment = f"RSI at {rsi:.1f} – Neutral momentum."
    trend = ""
    if pd.notna(sma20) and pd.notna(sma50):
        if sma20 > sma50:
            trend = "SMA20 above SMA50 – short-term uptrend."
        else:
            trend = "SMA20 below SMA50 – short-term downtrend."
    return (
        f"📊 <b>XAUUSD Technical Overview</b>\n\n"
        f"🔹 Current Price: ${price:.2f}\n"
        f"🔹 Change: {change:+.2f}%\n\n"
        f"📊 {rsi_comment}\n"
        f"📈 {trend}\n\n"
        f"<i>Data: Yahoo Finance | Educational purpose only</i>\n"
        f"#XAUUSD #GoldAnalysis #Educational"
    )

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    return requests.post(url, json={
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }).json()

def main():
    print("🔍 Fetching XAUUSD data...")
    df = fetch_gold_data()
    indicators = compute_indicators(df)
    msg = None
    if GEMINI_API_KEY:
        print("🤖 Using Gemini for analysis...")
        msg = generate_ai_analysis(indicators)
    if not msg:
        print("📋 Falling back to simple analysis...")
        msg = generate_simple_analysis(indicators)
    res = send_to_telegram(msg)
    if res.get('ok'):
        print("✅ Analysis posted to channel.")
    else:
        print("❌ Failed:", res)

if __name__ == "__main__":
    main()
