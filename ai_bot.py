#!/usr/bin/env python3
"""
Rawatbhata Direct AI Bot — Groq powered (FREE, fast)
Keys loaded from Windows environment variables (GROQ_API_KEY, TG_BOT_TOKEN)
"""
import logging, os, json, urllib.request, ssl, time, subprocess, sys, requests
from datetime import datetime

# ─── KEYS FROM ENVIRONMENT ────────────────────────────────
# Set these once in Windows: 
#   setx GROQ_API_KEY "your_key"
#   setx TG_BOT_TOKEN "your_token"
GROQ_KEY  = os.environ.get("GROQ_API_KEY", "")
TOKEN     = os.environ.get("TG_BOT_TOKEN", "")
CHAT_ID   = int(os.environ.get("TG_CHAT_ID", "0"))

if not GROQ_KEY:
    print("ERROR: GROQ_API_KEY not set. Run: setx GROQ_API_KEY \"your_key\"")
    sys.exit(1)
if not TOKEN:
    # Fallback: read from .token file
    token_file = os.path.join(os.path.dirname(__file__), ".token")
    if os.path.exists(token_file):
        TOKEN = open(token_file).read().strip()

GROQ_API   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "groq/compound-mini"

CTX_FILE  = os.path.join(os.path.dirname(__file__), "context.json")
LOG_FILE  = os.path.join(os.path.dirname(__file__), "ai_bot.log")

# ─── LOGGING ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ─── SSL ───────────────────────────────────────────────────
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ─── TELEGRAM HELPERS ──────────────────────────────────────
API = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=0):
    url = f"{API}/getUpdates?offset={offset}&timeout=3&allowed_updates=message"
    req = urllib.request.urlopen(url, context=ctx, timeout=10)
    return json.loads(req.read())

def send_message(chat_id, text, parse_mode="Markdown"):
    if len(text) > 4096:
        for i in range(0, len(text), 4096):
            send_message(chat_id, text[i:i+4096], parse_mode)
        return
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False
    }).encode()
    req = urllib.request.Request(f"{API}/sendMessage", data=payload,
                                  headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, context=ctx, timeout=15)

def send_typing(chat_id):
    payload = json.dumps({"chat_id": chat_id, "action": "typing"}).encode()
    req = urllib.request.Request(f"{API}/sendChatAction", data=payload,
                                  headers={"Content-Type": "application/json"})
    try: urllib.request.urlopen(req, context=ctx, timeout=5)
    except: pass

# ─── CONTEXT (conversation memory) ────────────────────────
def load_ctx():
    if os.path.exists(CTX_FILE):
        with open(CTX_FILE) as f:
            return json.load(f)
    return {"messages": [], "last_update": None}

def save_ctx(data):
    with open(CTX_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False)

# ─── GROQ AI CALL ─────────────────────────────────────────
SYSTEM_PROMPT = """Tu Rawatbhata Direct ka AI assistant hai.
User ka naam Pankaj hai, woh Rawatbhata (Rajasthan) se hai.
Woh Telegram se baat kar raha hai — tu uska personal AI bot hai jo PC pe chal raha hai.
Usne ek hyperlocal delivery app banaya hai: rawatbhata-hyperlocal.vercel.app
Woh is app ko launch kar raha hai — marketing, vendor onboarding, driver recruitment, Instagram content, WhatsApp broadcast sab uska kaam hai.

Tere powers (agar user kaam de toh):
- Code likh sakta hai, execute bhi kar sakta hai (subprocess)
- Cronjobs bana aur manage kar sakta hai (hermes cron)
- Memory update kar sakta hai
- Files padh aur likh sakta hai
- Web search kar sakta hai
- Telegram se message bhej sakta hai
- WhatsApp, Instagram ka content bana sakta hai

Guidelines:
- Hinglish me jawab do (Hindi + English mixed, natural)
- Short aur direct — boss ko lamba reply nahi chahiye
- Jab kaam ho jaye, sirf "✅ Done" ya "🎉 [result]" likh
- Jab user koi kaam de, turant shuru kar — soch mat, execute kar
- Agar kuch install/dependancy chahiye toh bata dena
- Agar tu kuch naya build karein (image, script, file) toh summary batana
- Memory check karne ke baad info update bhi kar sakta hai agar user ne naya fact bataya

Memory facts:
- Pankaj ka IG: @the.musafirrr__
- App: rawatbhata-hyperlocal.vercel.app
- PIN: 323303, Rawatbhata, Chittorgarh, Rajasthan
- Telegram bot: @Pbx14lBot
- Brand color: Amber #f59e0b + Slate #0f172a
- Tagline: "Baithe raho, kaam ho jayega."
- Budget: ₹0 (zero budget)
- PC: Windows 11, i7-12700, 64GB RAM
- n8n VPS server bhi hai (cloud)
"""

def ask_ai(user_text, chat_id):
    ctx_data = load_ctx()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in ctx_data["messages"][-10:]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_text})

    try:
        resp = requests.post(
            GROQ_API,
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.7,
            },
            timeout=30
        )
        result = json.loads(resp.text)
        reply = result["choices"][0]["message"]["content"].strip()

        ctx_data["messages"].append({"role": "user", "content": user_text})
        ctx_data["messages"].append({"role": "assistant", "content": reply})
        ctx_data["last_update"] = str(datetime.now())
        if len(ctx_data["messages"]) > 40:
            ctx_data["messages"] = ctx_data["messages"][-40:]
        save_ctx(ctx_data)

        return reply
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return f"AI error: {e}"

# ─── MESSAGE HANDLER ───────────────────────────────────────
def handle_message(text, chat_id, first_name):
    text = text.strip()

    if chat_id != CHAT_ID:
        logger.warning(f"Unauthorized: {chat_id}")
        return

    send_typing(chat_id)

    if text.lower() in ["/start", "start", "/help", "hi", "hello", "hey", "namaste"]:
        send_message(chat_id,
            f"👋 Namaste {first_name}!\n\n"
            "Rawatbhata Direct AI Bot live hai.\n"
            "Mujhe kuch bhi puchho ya kaam bolo — main kar dunga.\n\n"
            "Examples:\n"
            "• 'Aaj ka plan bana'\n"
            "• 'Rawatbhata ka IG post bana'\n"
            "• 'Vendor script likh de'\n"
            "• 'Kal 9 baje reminder bhejo'\n"
            "• 'Leads tracker khol'\n"
            "• 'Kuch bhi puchho!'\n\n"
            "Sab kuch ho jayega! 🚀"
        )
        return

    if text == "/ctx":
        ctx_data = load_ctx()
        send_message(chat_id, f"Context: {len(ctx_data.get('messages', []))} messages stored")
        return

    if text == "/reset":
        save_ctx({"messages": [], "last_update": str(datetime.now())})
        send_message(chat_id, "✅ Context cleared. Memory fresh.")
        return

    if text == "/status":
        send_message(chat_id,
            f"✅ Bot: ONLINE\n"
            f"👤 Owner: {first_name}\n"
            f"💬 Chat ID: {chat_id}\n"
            f"🤖 AI: Groq (compound-mini)\n"
            f"📁 Context: {len(load_ctx().get('messages', []))} messages"
        )
        return

    reply = ask_ai(text, chat_id)
    logger.info(f"AI: {reply[:80]}")
    send_message(chat_id, reply)

# ─── MAIN LOOP ─────────────────────────────────────────────
def main():
    logger.info("=" * 50)
    logger.info("Rawatbhata Direct AI Bot — STARTING")
    logger.info(f"Chat ID: {CHAT_ID} | AI: Groq compound-mini")
    logger.info("=" * 50)

    try:
        test = ask_ai("Hello", CHAT_ID)
        logger.info(f"Groq OK: {test[:50]}")
        send_message(CHAT_ID, "✅ Rawatbhata Direct AI Bot — LIVE!\n\nGroq connected.\n\nKuch bhi pucho ya kaam bolo — main ready hoon! 🚀")
    except Exception as e:
        logger.error(f"Groq failed: {e}")
        send_message(CHAT_ID, f"⚠️ AI not connected: {e}\n\nBot running but AI offline.")

    offset = 0
    while True:
        try:
            updates = get_updates(offset)
            for u in updates.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                first_name = msg.get("from", {}).get("first_name", "Boss")
                if text:
                    handle_message(text, chat_id, first_name)
        except Exception as e:
            logger.error(f"Loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
