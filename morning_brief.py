import requests
import json
from datetime import datetime

import os

# Read the actual bot token from environment
token = os.environ.get("TG_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TG_CHAT_ID", "")

# Today's date in Hindi format
today = datetime.now()
hindi_months = {
    1: "जनवरी", 2: "फरवरी", 3: "मार्च", 4: "अप्रैल",
    5: "मई", 6: "जून", 7: "जुलाई", 8: "अगस्त",
    9: "सितंबर", 10: "अक्टूबर", 11: "नवंबर", 12: "दिसंबर"
}
hindi_date = f"{today.day} {hindi_months[today.month]} {today.year}"

briefing = f"""🗞️ *RAWATBHATA MORNING BRIEF*
📅 {hindi_date}

📰 *आज की खबरें:*
1. ⚠️ *CISF जवान की मौत, परमाणु संयंत्र में फायरिंग की घटना* — रावतभाटा परमाणु विद्युत संयंत्र में तैनात 25 वर्षीय CISF जवान की गोली लगने से मौत, जांच जारी। (टाइम्स ऑफ इंडिया)
2. 🏛️ *रावतभाटा नगरपालिका चुनाव 2026: नामांकन की अंतिम तिथि तय* — दैनिक भास्कर के अनुसार आगामी नगरपालिका चुनाव के लिए नामांकन की समय सीमा निर्धारित।
3. 🤒 *कोटा: 27 बच्चे बीमार, मिड-डे मील खाने से उल्टी-चक्कर* — सरकारी स्कूल में मध्याह्न भोजन के बाद 27 बच्चों की तबीयत बिगड़ी, सभी स्थिर।
4. 🌧️ *चित्तौड़गढ़ में बारिश का इंतजार* — बादल छाए, गरज के साथ बिजली लेकिन कोई बारिश नहीं; मानसून से राहत नहीं।
5. 🎬 *रावतभाटा लेटेस्ट वीडियो न्यूज — 27 अगस्त 2026* — स्थानीय वीडियो न्यूज में ताज़ा घटनाएं और रिपोर्ट।
6. 📢 *रावतभाटा: 29 अगस्त की ताज़ा खबरें* — दैनिक भास्कर में आज की स्थानीय खबरों का विस्तृत कवरेज।

🌤️ *आज का मौसम:* ☁️ आंशिक रूप से धूप, अधिकतम 33°C (92°F), न्यूनतम 25°C (77°F) | शुक्रवार से बारिश की संभावना 🌧️

💡 *डिलीवरी टिप:* बरसात शुरू होने से पहले अपनी वाहन की ब्रेक और टायर ज़रूर चेक कर लें — सड़कें गीली होने पर रिक्शे की ब्रेकिंग दूरी बढ़ जाती है। सुरक्षित दूरी बनाए रखें!

🤖 — Rawatbhata Direct Bot | rawatbhata-hyperlocal.vercel.app"""

def send_telegram(text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    print("Status:", r.status_code)
    print("Response:", r.text)
    return r

print("Sending morning brief to Telegram...")
result = send_telegram(briefing)
print("\nDone!" if result.status_code == 200 else "\nFailed!")
