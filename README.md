# 🤖 Telegram AI Concierge & Morning Briefing Bot

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot_API-2CA5E0?style=for-the-badge&logo=telegram)](https://core.telegram.org/bots/api)
[![Groq](https://img.shields.io/badge/Groq-Fast_LLM_Inference-F04D23?style=for-the-badge)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **An intelligent, autonomous Telegram AI Concierge and notification pipeline.** Delivers scheduled daily morning briefings, dynamic contextual AI interactions powered by Groq/LLaMA, whitelist user access control, and automated broadcast campaigns.

---

## 🌟 Features & Capabilities

- ⚡ **Ultra-Fast LLM Intelligence**: Powered by Groq's high-speed inference engine (Llama-3/Mixtral) for instant conversational responses.
- 🌅 **Automated Morning Briefings**: Dispatches localized weather, news, priority tasks, and daily reminders directly to subscribers.
- 🛡️ **Role-Based Authorization Whitelist**: Restricts sensitive commands and access strictly to verified user IDs (`authorized_users.json`).
- 📢 **Broadcast Campaign Engine**: Includes JSON playbooks (`content/broadcasts.json`) for targeted announcements and content scheduling.
- 🪶 **Dual Architecture**:
  - `ai_bot.py`: Complete LLM-powered conversational concierge with session memory.
  - `bot_simple.py`: Zero-dependency, ultra-lightweight fallback using pure Python standard library (`urllib`).
- 🔄 **Background & Daemon Execution**: Native Windows VBS background launcher (`silent_start.vbs`) and Linux systemd service compatibility.

---

## 🚀 Quick Start Guide

### 1. Installation
```bash
git clone https://github.com/pixelssudio/telegram-ai-concierge.git
cd telegram-ai-concierge
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` or set environment variables:
```bash
cp .env.example .env
```
Fill in your credentials:
```env
TG_BOT_TOKEN=your_telegram_bot_token_from_botfather
TG_CHAT_ID=your_telegram_user_id
GROQ_API_KEY=your_groq_api_key
```

### 3. Authorize Users
Edit `authorized_users.json` with your Telegram User ID (retrieved from [@userinfobot](https://t.me/userinfobot)):
```json
{
  "ids": [YourTelegramID],
  "owner": YourTelegramID
}
```

### 4. Run the Bot
```bash
# Start AI Bot
python ai_bot.py

# Or run the instant morning brief test
python morning_brief.py
```

---

## 📂 Repository Structure

```text
├── content/
│   ├── broadcasts.json   # Scheduled announcement sequences
│   ├── playbook.json     # Conversion & dialogue scripts
│   └── reels.json        # Video script prompts & templates
├── ai_bot.py             # Main Groq-powered AI conversational bot
├── bot_simple.py         # Zero-dependency lightweight Telegram bot
├── morning_brief.py      # Automated daily briefing generator
├── context.json          # System prompts & knowledge base context
├── authorized_users.json # Whitelist user configuration
├── requirements.txt      # Dependencies
└── .env.example          # Environment variables template
```

---

## 💼 Freelance & Custom Bot Development Services

Looking for a custom Telegram bot for your business, community, or customer support?

I offer turnkey custom bot solutions:
- 🤖 **AI Customer Support & Lead Capture Bots**
- 💳 **Telegram Payment Bots** (Stripe, Crypto, UPI)
- 📊 **Trading Alerts & Exchange Webhook Dispatchers** (TradingView ➔ Telegram)
- 🔒 **Private Paid Community Subscription & Access Control Bots**

**Hire me for freelance projects:**
- 📧 **Email**: Available via GitHub profile
- 💬 **Telegram**: [@the_musafir](https://t.me/the_musafir)
- 💼 **Upwork / Fiverr**: Available for hire

---

## 📄 License
MIT License. Built by **[the.musafir](https://github.com/pixelssudio)** — Full-Stack AI Engineer.
