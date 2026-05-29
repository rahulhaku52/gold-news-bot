import os, requests

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

print("========== DIAGNOSTIC ==========")
print("BOT_TOKEN starts with:", BOT_TOKEN[:10] if BOT_TOKEN else "NOT SET")
print("CHANNEL_ID read by Action:", repr(CHANNEL_ID))  # repr দিলে স্পেস/হিডেন ক্যারেক্টার ধরা পড়বে

# টেস্ট মেসেজ পাঠাই
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHANNEL_ID,
    "text": "🔍 Action Diagnostic: CHANNEL_ID = " + str(CHANNEL_ID),
    "parse_mode": "HTML"
}
try:
    resp = requests.post(url, json=payload, timeout=10)
    print("Response status:", resp.status_code)
    print("Response body:", resp.text[:500])
except Exception as e:
    print("Request failed:", e)
