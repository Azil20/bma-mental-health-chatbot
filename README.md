# 🌿 BMA — Mental Health Chatbot

> **BMA** is an AI-powered mental health support companion that provides empathetic, non-judgmental emotional support using the Claude LLM and a fine-tuned DistilBERT intent classifier.

**Created by:** Bilal Jellaoui · Mohammed Azil · Ayoube Echihami

---

## 📁 Project Structure

```
mental_health_chatbot/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── routes.py                # API endpoints (/chat, /mood, /stats...)
│   ├── models/
│   │   ├── chat_model.py        # Claude LLM wrapper
│   │   ├── nlp_classifier.py    # DistilBERT intent classifier
│   │   └── saved_model/         # Fine-tuned model weights (auto-generated)
│   ├── services/
│   │   ├── safety.py            # Crisis detection module
│   │   └── memory.py            # SQLite conversation memory
│   └── templates/
│       ├── index.html           # Chat interface
│       └── dashboard.html       # Analytics & mood tracker
├── ml/
│   ├── preprocess.py            # Tokenisation + data cleaning + splits
│   ├── train.py                 # Fine-tune DistilBERT
│   ├── evaluate.py              # F1, accuracy, confusion matrix
│   └── processed/               # Auto-generated train/val/test JSON splits
├── data/
│   ├── intents.json             # 24 intent tags across 10 classes (English)
│   └── emotions.csv             # 100 labeled emotion samples
├── notebooks/
│   └── eda_emotion_analysis.py  # EDA plots + dataset report
├── database/
│   └── mental_health.db         # SQLite database (auto-created)
├── config.py                    # App settings
├── .env                         # API keys (never commit!)
├── requirements.txt             # Python dependencies
├── run.py                       # App entry point
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & install

```bash
git clone https://github.com/your-repo/bma-chatbot.git
cd bma-chatbot
pip install -r requirements.txt
```

### 2. Set your API key

Edit `.env`:

```env
GROQ_API_KEY=your_key_here
```

### 3. Run the app

```bash
python run.py
```

Open:
- **Chat** → `http://localhost:5000`
- **Dashboard** → `http://localhost:5000/dash`

---

## 🤖 ML Pipeline (Optional Fine-tuning)

> Fine-tuning is optional. BMA works out of the box with Claude API + keyword fallback.

```bash
# Step 1 — Preprocess & split data
python ml/preprocess.py

# Step 2 — Fine-tune DistilBERT (requires GPU recommended)
python ml/train.py --epochs 10 --batch_size 16

# Step 3 — Evaluate the model
python ml/evaluate.py

# Step 4 — Explore the dataset (EDA)
python notebooks/eda_emotion_analysis.py
```

---

## 🌐 API Reference

| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | `/api/session/start` | Create a new session                 |
| POST   | `/api/chat`          | Send a message, get BMA's response   |
| POST   | `/api/mood`          | Log a mood score (1–10)              |
| GET    | `/api/mood/history`  | Get mood history for a session       |
| GET    | `/api/stats`         | Global usage statistics              |
| POST   | `/api/feedback`      | Submit a rating for a response       |
| GET    | `/api/health`        | Health check                         |

### Example — Start a session

```bash
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'
```

### Example — Send a message

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "I feel really anxious today"
  }'
```

---

## 🗂️ Dataset — Intent Classes

| Class                  | Tags covered                                      | Samples |
|------------------------|---------------------------------------------------|---------|
| `greeting_farewell`    | greeting, goodbye                                 | 27      |
| `bot_identity`         | about_bot, creators                               | 18      |
| `emotional_support`    | sadness, anxiety, anger, happiness, loneliness    | 55+     |
| `stress_management`    | work/study stress, financial stress               | 28      |
| `relationships_social` | relationships, social/digital pressure            | 24      |
| `self_growth`          | self-esteem, grief/loss, mindfulness, boundaries  | 33      |
| `crisis_safety`        | crisis/self-harm, abuse, medication               | 24      |
| `lifestyle_wellness`   | sleep, addiction, faith/Ramadan                   | 27      |
| `professional_resources` | therapist, help resources                       | 14      |
| `general_interaction`  | thanks, compliments/insults                       | 20      |

---

## 🛡️ Crisis Safety

BMA includes a **dedicated crisis detection module** (`app/services/safety.py`) that:

- Scans every message **before** the LLM using keyword patterns
- Classifies severity: `none` → `low` → `medium` → `high` → `critical`
- Appends crisis resources automatically when triggered
- Logs all crisis events to the database

**Emergency lines displayed by BMA:**
- 🇲🇦 Morocco: **0801 000 180**
- 🌍 International: **befrienders.org**
- 🇺🇸 US: **988**

---

## 🏗️ Architecture

```
User Message
     │
     ▼
CrisisDetector (safety.py)   ← fast keyword scan, <1ms
     │
     ▼
ConversationMemory (memory.py) ← load last 10 turns from SQLite
     │
     ▼
BMAChat (chat_model.py) ← Claude API + specialized system prompt
     │
     ▼
IntentClassifier (nlp_classifier.py) ← DistilBERT / keyword fallback
     │
     ▼
Response + Intent Class
     │
     ▼
ConversationMemory ← persist message + crisis log if needed
```

---

## 📊 Database Schema (SQLite)

```sql
sessions        -- user sessions (language, initial mood)
messages        -- full conversation history
mood_logs       -- daily mood scores (1–10)
crisis_events   -- flagged crisis messages
feedback        -- user ratings (1–5 stars)
```

---

## 🔮 Roadmap

- [ ] JWT authentication for multi-user support
- [ ] Therapist admin dashboard with session overview
- [ ] PostgreSQL migration for production scale
- [ ] Mobile app (React Native)
- [ ] Arabic / Darija language dataset expansion
- [ ] Fine-tuned model with 500+ examples

---

## ⚠️ Disclaimer

**BMA is not a substitute for professional mental health care.**
If you are in crisis, please contact a licensed therapist or emergency services immediately.

---

*BMA v1.0.0 · MIT License · Created with love by Bilal Jellaoui, Mohammed Azil, Ayoube Echihami*
