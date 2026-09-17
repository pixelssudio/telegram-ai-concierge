#!/usr/bin/env python3
"""Minimal Rawatbhata Direct Bot — pure urllib, no dependencies"""
import logging, os, json, urllib.request, ssl, time

TOKEN = os.environ.get("TG_BOT_TOKEN", "")
CHAT_ID = int(os.environ.get("TG_CHAT_ID", "0"))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

API = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

def get_updates(offset=0):
    url = f"{API}/getUpdates?offset={offset}&timeout=3"
    req = urllib.request.urlopen(url, context=ctx, timeout=10)
    return json.loads(req.read())

def send_message(chat_id, text, parse_mode="Markdown"):
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }).encode()
    req = urllib.request.Request(f"{API}/sendMessage", data=payload, headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, context=ctx, timeout=10)

MENU = ("🤖 *Rawatbhata Direct Ops Bot - LIVE!*\n\n"
    "/menu - All commands\n"
    "/playbook - Today's 5-step plan\n"
    "/wa1 to /wa5 - WhatsApp messages\n"
    "/reel1 to /reel10 - Reel scripts\n"
    "/vendor - Vendor pitch script\n"
    "/driver - Driver pitch script\n"
    "/story - Story template ideas\n"
    "/install - App install guide\n"
    "/stats - Lead tracker\n"
    "/broadcast - WA broadcast guide\n\n"
    "Sab free hai, sab ready hai! 🚀")

PLAYBOOK = ("📋 *TODAY'S 5-STEP PLAN*\n\n"
    "✅ 9-10 AM - WA Msg 1 bhejo + Story post\n"
    "✅ 11 AM - WA Msg 2 + Reel 1 shoot\n"
    "✅ 1 PM - WA Msg 3 + Vendor walks\n"
    "✅ 5 PM - WA Msg 4 + Driver onboarding\n"
    "✅ 8 PM - WA Msg 5 + Stats update\n\n"
    "🎯 Goal: 10 installs, 3 vendors, 2 drivers")

COMMANDS = {
    "/menu": MENU,
    "/playbook": PLAYBOOK,
    "/today": PLAYBOOK,
    "/wa1": "🔥 *Rawatbhata Direct - FREE Delivery!*\n\nGhar baithe order karo! Food, grocery, medicines, rides - sab kuch.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "/wa2": "🍔 *Pizza, Chowmein, Biryani - ab ghar baithe!*\n\nRawatbhata ke sabse popular restaurants ab app pe.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "/wa3": "💊 Medical, Grocery, Paratha - jo chahiye, wo la do!\n\n1 click, free delivery.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "/wa4": "🛺 *Auto rickshaw, cab, goods carrier - book now!*\n\nRawatbhata me kahin bhi jao.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "/wa5": "📲 *App install karo, free delivery pao!*\n\nAdd to Home Screen - iOS/Android.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "/reel1": "📹 *Reel 1 - Auto Rickshaw*\n\n🎬 SHOOT:\n1. Rickshaw dikhao\n2. Driver se baat: 'App se booking hoti hai?'\n3. App dikhao\n4. Order book karte dikhao\n\n🎵 Trending audio\n⏱ 15-25 sec",
    "/reel2": "📹 *Reel 2 - No Zomato/Swiggy?*\n\n🎬 SHOOT:\n1. 'Delivery not available' dikhao\n2. SOUND: record scratch\n3. 'Ab Rawatbhata Direct use karo!'\n4. App pe order place karo\n\n🎵 Comedy audio\n⏱ 20-30 sec",
    "/reel3": "📹 *Reel 3 - Vendor/Dhaba*\n\n🎬 SHOOT:\n1. Local dhaba dikhao\n2. 'Rawatbhata Direct se order karo!'\n3. QR code dikhao\n\n🎵 Desi bgm\n⏱ 15-20 sec",
    "/reel4": "📹 *Reel 4 - Pain Point*\n\n🎬 SHOOT:\n1. Person frustrated on phone\n2. VOICE: 'Rawatbhata me delivery nahi milti?'\n3. App open karo, order place karo\n4. Delivery aati hai\n\n🎵 Comedy\n⏱ 20-30 sec",
    "/reel5": "📹 *Reel 5 - App Install*\n\n🎬 SHOOT:\n1. Browser kholo\n2. rawatbhata-hyperlocal.vercel.app\n3. Share > Add to Home Screen\n4. App icon banta hai\n\n🎵 Trending audio\n⏱ 15-20 sec",
    "/install": "📱 *App Install Guide*\n\n👉 rawatbhata-hyperlocal.vercel.app\n\n*iOS:* Safari > Share > Add to Home Screen\n*Android:* Chrome > 3-dot > Install app\n\n💡 Free, no app store needed!",
    "/stats": "📊 *Lead Tracker*\n\n📁 File: 05-Lead-Tracker.xlsx\n📁 Location: Rawatbhata-Direct-Launch/\n\nManually update karo entries.",
    "/vendor": "🏪 *VENDOR SCRIPT*\n\n'Namaste bhaiya, main Pankaj. Maine Rawatbhata Direct app banaya. Ispe log order karenge, aapki dukaan se delivery hogi. Commission ₹0. Kya join karna chahenge?'\n\n💡 Demo: Apne phone pe app dikhao. QR code do.",
    "/driver": "🚗 *DRIVER SCRIPT*\n\n'Namaste bhaiya, main Pankaj. Rawatbhata Direct app se ride bookings aayenge. Commission ₹0. Basic smartphone enough hai.'\n\n💡 Demo: App dikhao, ride accept karna dikhao.",
    "/story": "📸 *STORY IDEAS*\n\n1️⃣ 30% OFF First Order - Story-1-Offer-30OFF.png\n2️⃣ QR Code - Scan & Order\n3️⃣ Your Shop on Rawatbhata Direct\n4️⃣ Earn Extra - Referral\n5️⃣ Referral Rs50 - Story-5-Referral-Rs50.png\n\nReady templates: Rawatbhata-Direct-Launch/Story-Templates/",
    "/broadcast": "📣 *WA BROADCAST GUIDE*\n\n1. WhatsApp > New Broadcast > +\n2. Contacts add karo\n3. Ek baar me 1 message\n4. /wa1 se /wa5 use karo\n\n⏰ Timing: 9AM, 1PM, 6PM",
}

def main():
    logger.info("Starting minimal bot...")
    offset = 0

    while True:
        try:
            updates = get_updates(offset)
            for u in updates.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                first_name = msg.get("from", {}).get("first_name", "")

                logger.info(f"MSG: '{text}' from {first_name} ({chat_id})")

                if chat_id == CHAT_ID:
                    if text in COMMANDS:
                        send_message(chat_id, COMMANDS[text])
                        logger.info(f"Replied: {text}")
                    elif text.startswith("/"):
                        send_message(chat_id, "Unknown command. /menu for all commands.")
                    elif text.lower() in ["hi", "hello", "start", "/start"]:
                        reply = (f"👋 Namaste {first_name}! Rawatbhata Direct Bot live hai!\n\n"
                                f"/menu for all commands - sab free hai!")
                        send_message(chat_id, reply)
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
