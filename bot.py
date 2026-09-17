#!/usr/bin/env python3
"""Rawatbhata Direct Ops Bot — Fixed version (no JobQueue)"""
import logging, json, os, threading, time
from datetime import datetime, time as dtime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# === CONFIG ===
TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".token")
TOKEN = open(TOKEN_FILE).read().strip()
BOT_CHAT_IDS = []
OWNER_ID = None

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# === CONTENT ===
WA_MSGS = [
    "🔥 *Rawatbhata Direct — FREE Delivery!*\n\nGhar baithe order karo! Food, grocery, medicines — sab kuch.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "🍔 *Pizza, Chowmein, Biryani* — ab ghar baithe!\n\nRawatbhata ke sabse popular restaurants ab app pe.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "💊 Medical, Grocery, Paratha — jo chahiye, wo la do!\n\n1 click, free delivery.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "🛺 *Rickshaw, Cab, Goods carrier* — book now!\n\nRawatbhata me kahin bhi jao, ₹0 commission.\n\n👉 rawatbhata-hyperlocal.vercel.app",
    "📲 *App install karo, free delivery pao!*\n\nAdd to Home Screen → iOS/Android dono.\n\n👉 rawatbhata-hyperlocal.vercel.app",
]

REEL_SCRIPTS = [
    ("Rickshaw/Wala", "📹 *Reel 1 — Rickshaw*

🎬 SHOOT:
1. Auto rickshaw b ground par
2. Driver se baat karo — 'Rawatbhata Direct se booking hoti hai?'
3. App dikhao
4. SHOOT: App pe order book karte hue
5. VOICE: 'Auto rickshaw ab app se book karo — ₹0 commission!'

🎵 Trending audio
⏱ 15-25 sec"),
    ("Zomato/Swiggy Kaise", "📹 *Reel 2 — No Zomato/Swiggy?*

🎬 SHOOT:
1. Zomato/Swiggy pe 'Delivery not available' dikhao
2. SOUND: record scratch
3. VOICE: 'Ab Rawatbhata Direct use karo!'
4. App pe order place karo
5. Delivery aati dikhao
6. TEXT: 'Rawatbhata Direct — FREE Delivery'

🎵 Trending comedy audio
⏱ 20-30 sec"),
    ("Vendor/Dhaba", "📹 *Reel 3 — Vendor Apne Paas*

🎬 SHOOT:
1. Local dhaba/meat shop/selfie with vendor
2. VOICE: 'Yahan se order karo — Rawatbhata Direct pe!'
3. Vendor ko batana: 'App se zyada customers aayenge'
4. QR code dikhao
5. TEXT: 'Sab ke liye FREE'

🎵 Desi bgm
⏱ 15-20 sec"),
    ("Pain Point", "📹 *Reel 4 — Free Delivery Pain Point*

🎬 SHOOT:
1. SOUND: record scratch
2. Person looks frustrated on phone
3. VOICE: 'Rawatbhata me delivery nahi milti kisi cheez ki?'
4. App open karo
5. Order place karo
6. Delivery boy aata hai
7. TEXT: 'FREE Delivery — Rawatbhata Direct'

🎵 Comedy/trending
⏱ 20-30 sec"),
    ("App Install", "📹 *Reel 5 — Add to Home Screen*

🎬 SHOOT:
1. Phone me browser kholo
2. rawatbhata-hyperlocal.vercel.app daalo
3. Share button → Add to Home Screen
4. App icon banta hai
5. VOICE: 'Yeh app iPhone/Android dono pe kaam karta hai!'

🎵 Trending audio
⏱ 15-20 sec"),
    ("Groceries", "📹 *Reel 6 — Grocery Karo*

🎬 SHOOT:
1. Kitchen shelf empty
2. Phone leke baitho
3. App kholo, grocery add karo
4. Order confirm
5. VOICE: 'Rashan, aata, oil — sab free delivery!'

🎵 Light bgm
⏱ 15 sec"),
    ("Medicine", "📹 *Reel 7 — Medicines*

🎬 SHOOT:
1. Prescription dikhao
2. App kholo
3. Medicine search karo
4. Order place
5. VOICE: 'Medicines bhi ghar baithe — Rawatbhata Direct!'

🎵 Calm/trust bgm
⏱ 15 sec"),
    ("Ride Share", "📹 *Reel 8 — Ride Share*

🎬 SHOOT:
1. Person platform pe khada
2. App kholo
3. Ride book karo
4. Rickshaw/cab aati hai
5. VOICE: 'Rawatbhata me ride bhi app se!'

🎵 Trending audio
⏱ 15 sec"),
    ("Friend Referral", "📹 *Reel 9 — Referral*

🎬 SHOOT:
1. Dost ko dikhayo app
2. Bol: 'Yeh app free hai, share kar!'
3. QR code scan
4. Both get free delivery
5. VOICE: 'Refer karo, free delivery pao!'

🎵 Fun bgm
⏱ 15 sec"),
    ("Launch/Azadi", "📹 *Reel 10 — Grand Launch*

🎬 SHOOT:
1. Cinematic shot of Rawatbhata
2. Text: 'RAWATBHATA DIRECT LAUNCH!'
3. App dikhao
4. All services shown
5. VOICE: 'Rawatbhata ka sabse bada launch! FREE Delivery — Sab ke liye!'
6. TEXT: 'rawatbhata-hyperlocal.vercel.app'

🎵 Inspiring/energetic
⏱ 25-30 sec"),
]

TODAY_PLAN = """📋 *RAWATBHATA DIRECT — AAJ KA PLAN*

✅ *Step 1 — Morning (9-10 AM)*
WA Broadcast Msg 1 bhejo (group/contacts)
Insta story post karo (Story-1-Offer-30OFF.png)

✅ *Step 2 — Late Morning (11 AM)*
WA Msg 2 bhejo
Instagram Reel 1 shoot karo (rickshaw)

✅ *Step 3 — Afternoon (1 PM)*
WA Msg 3 bhejo
Vendor walks — nearest 3 shops visit karo

✅ *Step 4 — Evening (5 PM)*
WA Msg 4 bhejo
Driver onboarding — 2 auto drivers bol

✅ *Step 5 — Night (8 PM)*
WA Msg 5 bhejo (CTA)
Story template 5 post karo (Referral)
Daily stats update karo /stats se

🎯 *Goal: 10 installs, 3 vendors, 2 drivers*"""

MENU = """🤖 *Rawatbhata Direct Ops Bot*

📋 /playbook — Aaj ka 5-step plan
📱 /install — App install kaise karte hain
📊 /stats — Lead tracker summary
📣 /wa1-5 — WhatsApp messages
🎬 /reel1-10 — Reel scripts
👥 /vendor — Vendor script
🚗 /driver — Driver script
📸 /story — Story template idea
💬 /broadcast — WA broadcast guide

*Sab free hai, sab ready hai!* 🚀"""

VENDOR_SCRIPT = """🏪 *VENDOR OUTREACH SCRIPT*

📢 *DOOR-TO-DOOR VENDOR WALK*

*APPROACH:*
"Namaste bhaiya/ben, Pankaj bol raha hoon Rawatbhata se.
Maine ek app banaya hai — Rawatbhata Direct.
Ispe log order karenge, aapki dukaan se delivery hogi.
*Commission ₹0.* Sirf 5% platform fee (customer se).

*BAAT KARNE KA TARIKA:*
1. Pehle appreciation: "Bahut acchi dukaan hai!"
2. Phir problem pucho: "Aapko customers ke liye problem kya hoti hai?"
3. Solution do: "Mera app aapki dukaan ko FREE promote karega"
4. Demo do: Apne phone pe rawatbhata-hyperlocal.vercel.app dikhao
5. QR code: Vendor ko QR dede — customer scan kare, order aaye

*SCRIPT:*
"Listen bhaiya, main Pankaj hoon. Maine Rawatbhata ke liye ek app banaya hai jahan log food, grocery, medicines order karte hain. Aapki dukaan se delivery hogi — aapko kuch dene ka nahi, sirf item dena hai. Commission zero. Kya aap join karna chahenge?"

*OBJECTION HANDLING:*
❌ "Mobile nahi aata" → "Koi nahi, QR code se kaam hoga"
❌ "Logo ko aata nahi" → "Main推广 karunga, aap sirf item ready rakhho"
❌ "Bahut app hain" → "Ye Rawatbhata ka apna app hai, local"

*CLOSE:*
"QR code scan karo, naam batao — kal se order aane lenge!"

*INCENTIVE TO CLOSE:* "First 10 orders pe FREE推广 (worth ₹500)"""

DRIVER_SCRIPT = """🚗 *DRIVER OUTREACH SCRIPT*

📢 *AUTO RICKSHAW / DRIVER WALK*

*APPROACH:*
"Namaste bhaiya, kya aap Rawatbhata me rickshaw/chhota rikshaw chalate hain?"

*BAAT:*
1. Pehle rapport banao: "Kaam kaisa chal raha hai?"
2. Problem: "Passengers ke liye paise dene ke alawa koi dikkat?"
3. Solution: "Mera app aapko ride bookings dega — phone pe notification aayega"

*SCRIPT:*
"Bhaiya, main Pankaj hoon. Maine Rawatbhata Direct app banaya hai jahan log rides book karte hain app se. Aapko sirf notification aayega, acceptance aapka. *Commission ₹0.* Ride accept karo, passenger pick karo, paise lo.

*DEMO:*
1. App dikhao (rawatbhata-hyperlocal.vercel.app)
2. Ride booking flow dikhayo
3. Kaha: "Dekho, itna simple!"

*INCENTIVE:* "First 50 rides pe ₹0 commission (worth ₹250)"

*OBJECTIONS:*
❌ "Phone nahi aata" → "Basic smartphone enough hai, ₹2000 wala bhi chalega"
❌ "Paise nahi aate" → "Payment directly aapke bank me UPI se"

*CLOSE:* "Number do, QR code bana deta hoon, kal se kaam shuru!""""

STORY_IDEA = """📸 *STORY TEMPLATE IDEAS*

1️⃣ *Offer:* "30% OFF First Order!"
   → Story-1-Offer-30OFF.png use karo

2️⃣ *QR Code:* "Scan & Order Now!"
   → App URL: rawatbhata-hyperlocal.vercel.app

3️⃣ *Vendor:* "Your Shop on Rawatbhata Direct!"
   → Screenshot of your shop, add QR overlay

4️⃣ *Driver:* "Earn Extra with Rickshaw!"
   → Rickshaw photo, referral code

5️⃣ *Referral:* "Refer & Get FREE Delivery!"
   → Story-5-Referral-Rs50.png use karo

💡 *Tip: Poll sticker use karo — 'Kya aapne Rawatbhata Direct try kiya?' / Yes / No*"""

def save_ids():
    with open("authorized_users.json", "w") as f:
        json.dump({"ids": BOT_CHAT_IDS, "owner": OWNER_ID}, f, indent=2)

def load_ids():
    global BOT_CHAT_IDS, OWNER_ID
    if os.path.exists("authorized_users.json"):
        data = json.load(open("authorized_users.json"))
        BOT_CHAT_IDS = data.get("ids", [])
        OWNER_ID = data.get("owner")

async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global OWNER_ID
    chat_id = update.effective_user.id
    if OWNER_ID is None:
        OWNER_ID = chat_id
        BOT_CHAT_IDS.append(chat_id)
        save_ids()
        await update.message.reply_text(
            "🎉 *Bot connected!*

Tumhara Telegram ID save ho gaya.
Ab yeh bot sirf tumhe responses degi.

/menu for all commands",
            parse_mode="Markdown"
        )
        logger.info(f"Owner registered: {chat_id}")
    elif chat_id == OWNER_ID:
        await update.message.reply_text("👋 Welcome back, Boss!

/menu for all commands", parse_mode="Markdown")
    else:
        await update.message.reply_text("⛔ Access denied.")

async def menu_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU, parse_mode="Markdown")

async def playbook_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TODAY_PLAN, parse_mode="Markdown")

async def wa_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.strip().lower()
    idx = int(cmd[-1]) - 1
    if 0 <= idx < len(WA_MSGS):
        msg = WA_MSGS[idx]
        await update.message.reply_text(msg, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("Usage: /wa1 to /wa5", parse_mode="Markdown")

async def reel_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.strip().lower()
    idx = int(cmd[-1]) - 1
    if 0 <= idx < len(REEL_SCRIPTS):
        title, script = REEL_SCRIPTS[idx]
        await update.message.reply_text(f"🎬 *{title}*

{script}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Usage: /reel1 to /reel10", parse_mode="Markdown")

async def vendor_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(VENDOR_SCRIPT, parse_mode="Markdown")

async def driver_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(DRIVER_SCRIPT, parse_mode="Markdown")

async def story_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(STORY_IDEA, parse_mode="Markdown")

async def install_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    install = """📱 *App Kaise Install Karein (iOS/Android — FREE)*

🌐 *Step 1 — Browser kholo*
Safari (iOS) ya Chrome (Android) me jaao:

👉 *rawatbhata-hyperlocal.vercel.app*

📱 *Step 2 — Add to Home Screen*

*iOS (Safari):*
1. Share button 🔗 dabavo (upward arrow)
2. "Add to Home Screen" dabao
3. "Add" dabao
✅ App icon home screen pe ho gaya!

*Android (Chrome):*
1. 3-dot menu ⋮ dabao
2. "Install app" ya "Add to Home Screen"
3. "Add" dabao
✅ App icon home screen pe ho gaya!

💡 *Ye PWA hai — app store se install ki zarurat nahi, bilkul free!*"""
    await update.message.reply_text(install, parse_mode="Markdown")

async def broadcast_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    guide = """📣 *WHATSAPP BROADCAST GUIDE*

⚠️ Pehle WhatsApp Broadcast List banavo:

1. WhatsApp kholo → New Broadcast → +
2. Jo contacts chahiye unhe add karo
3. Create karo

📋 *Broadcast karne ka tarika:*
• Ek baar me 1 hi message bhejo
• Messages alag-alag bhejo (no copy-paste sabko same)
• Sabse best: voice message bhejo — personal feel deta hai

⏰ *Timing:*
• Morning 9-10 AM — breakfast order
• Afternoon 1-2 PM — lunch
• Evening 6-7 PM — dinner/snacks

✅ *BAAD ME:* /wa1 se /wa5 messages use karo"""
    await update.message.reply_text(guide, parse_mode="Markdown")

async def stats_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    stats = """📊 *LEAD TRACKER — Rawatbhata Direct*

📁 *Sabse recent file:* `05-Lead-Tracker.xlsx`
📁 *Location:* `Rawatbhata-Direct-Launch/`

*Manually update karo Excel me:*
• Vendors — naam, type, contact, status
• Drivers — naam, vehicle, contact, status
• Customers — install karna hai toh yahan track karo

💡 *Bot apne aap tracking nahi kar sakti — tu entries add kar*"""
    await update.message.reply_text(stats, parse_mode="Markdown")

async def unknown(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Unknown command. /menu for all commands.")

# === SCHEDULER (threading-based) ===
def schedule_daily_morning():
    """9 AM push to owner — runs every day"""
    while True:
        now = datetime.now()
        next_run = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now >= next_run:
            next_run += __import__('datetime').timedelta(days=1)
        delay = (next_run - now).total_seconds()
        logger.info(f"Scheduler: next morning push in {delay/3600:.1f}h")
        time.sleep(delay)
        # Message will be sent when bot is running
        logger.info("9 AM push due — bot should be running")

def schedule_daily_evening():
    """8 PM push to owner — runs every day"""
    while True:
        now = datetime.now()
        next_run = now.replace(hour=20, minute=0, second=0, microsecond=0)
        if now >= next_run:
            next_run += __import__('datetime').timedelta(days=1)
        delay = (next_run - now).total_seconds()
        time.sleep(delay)
        logger.info("8 PM push due — bot should be running")

# === MAIN ===
def main():
    logger.info("Starting Rawatbhata Direct Ops Bot...")
    load_ids()
    
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler(["menu", "help"], menu_cmd))
    app.add_handler(CommandHandler("playbook", playbook_cmd))
    app.add_handler(CommandHandler("today", playbook_cmd))
    app.add_handler(CommandHandler("wa1", wa_msg))
    app.add_handler(CommandHandler("wa2", wa_msg))
    app.add_handler(CommandHandler("wa3", wa_msg))
    app.add_handler(CommandHandler("wa4", wa_msg))
    app.add_handler(CommandHandler("wa5", wa_msg))
    app.add_handler(CommandHandler("reel1", reel_cmd))
    app.add_handler(CommandHandler("reel2", reel_cmd))
    app.add_handler(CommandHandler("reel3", reel_cmd))
    app.add_handler(CommandHandler("reel4", reel_cmd))
    app.add_handler(CommandHandler("reel5", reel_cmd))
    app.add_handler(CommandHandler("reel6", reel_cmd))
    app.add_handler(CommandHandler("reel7", reel_cmd))
    app.add_handler(CommandHandler("reel8", reel_cmd))
    app.add_handler(CommandHandler("reel9", reel_cmd))
    app.add_handler(CommandHandler("reel10", reel_cmd))
    app.add_handler(CommandHandler("vendor", vendor_cmd))
    app.add_handler(CommandHandler("driver", driver_cmd))
    app.add_handler(CommandHandler("story", story_cmd))
    app.add_handler(CommandHandler("install", install_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    
    logger.info("Bot ready! polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
