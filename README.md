# 🌿 BMA — Mental Health Chatbot

> **BMA** is an empathetic, AI-powered mental health support companion built with a hybrid architecture combining a fine-tuned DistilBERT intent classifier, emotion detection, and Google Gemini LLM fallback.

**Created by:** Bilal Jellaoui · Mohammed Azil · Ayoube Echihami  
*(Master Big Data, Intelligence Artificielle et Applications Avancées — Morocco)*

---

## 📁 Project Structure

```
mental_health_chatbot/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── routes.py                # Web & API routes (/api/chat, /dashboard...)
│   ├── controllers/
│   │   └── chat_controller.py   # Hybrid ML + LLM + Multilingual orchestration
│   ├── models/
│   │   ├── user.py              # User model (SQLite)
│   │   ├── conversation.py      # Conversation management
│   │   └── database.py          # Database connection manager
│   ├── services/
│   │   ├── llm_service.py       # Google Gemini LLM with multi-model failover
│   │   ├── nlp_classifier.py    # DistilBERT intent classification
│   │   ├── emotion_detector.py  # Emotion classification model
│   │   ├── response_engine.py   # Dataset hit or LLM fallback decision engine
│   │   ├── safety.py            # Crisis detection & helpline referral
│   │   └── memory.py            # Conversation history & persistence
│   ├── utils/
│   │   ├── language_detector.py # Multilingual support (English, French, Arabic)
│   │   └── text_cleaner.py      # Text normalization utilities
│   └── templates/
│       ├── index.html           # Modern responsive chat interface
│       └── dashboard.html       # Analytics & mood tracker dashboard
├── config/
│   ├── config.py                # Central app configuration
│   └── logging_config.py        # Centralized logging setup
├── data/
│   ├── intents.json             # Mental health intents dataset
│   └── responses.json           # Curated response repository
├── ml/
│   ├── train.py                 # Training pipeline for ML models
│   ├── models/                  # Fine-tuned model checkpoints
│   └── tokenizer/               # Tokenizer and label encoders
├── notebooks/                   # EDA & data exploration notebooks
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules (protects API keys & large files)
├── requirements.txt             # Python dependencies
├── app.py                       # Main application entry point
├── run.py                       # Compatible entry point
├── test_pipeline.py             # End-to-end automated verification test suite
└── README.md                    # Project documentation
```

---

## ⚡ Quick Start

### 1. Clone & install

```bash
git clone https://github.com/Azil20/bma-mental-health-chatbot.git
cd bma-mental-health-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example file and add your Google Gemini API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Get a free Gemini API key at: https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL_NAME=gemini-flash-lite-latest
FLASK_DEBUG=True
PORT=5000
SECRET_KEY=bma-dev-secret
```

### 3. Run the App

```bash
python app.py
```

Open in your browser:
- **Chat Interface** → `http://localhost:5000`
- **Analytics Dashboard** → `http://localhost:5000/dashboard`

---

## 🧠 System Architecture

```
User Message (English / French / Arabic)
     │
     ▼
Language Detector & Normalizer (language_detector.py)
     │
     ▼
CrisisDetector (safety.py) ──────────────► [Triggered] ──► Immediate Crisis Helplines
     │ (Safe)
     ▼
Intent & Emotion Classifiers (DistilBERT)
     │
     ▼
Confidence >= 0.70?
     ├── YES ──► ResponseEngine (data/responses.json)
     └── NO  ──► Gemini LLM (llm_service.py) with Automatic Failover
                       (gemini-flash-lite-latest → gemini-3.1-flash-lite → ...)
     │
     ▼
Response Localization (Target Language)
     │
     ▼
Conversation Memory & SQLite Logging
```

---

## 🌐 API Endpoints

| Method | Endpoint             | Description                          |
|:-------|:---------------------|:-------------------------------------|
| `GET`  | `/`                  | Modern Chat Web App                  |
| `GET`  | `/dashboard`         | Analytics & Mood Dashboard           |
| `POST` | `/api/session/start` | Initialize a new session ID          |
| `POST` | `/api/chat`          | Send user message, get BMA response  |
| `POST` | `/api/mood`          | Log mood rating (1–10) with note     |
| `GET`  | `/api/mood/history`  | Retrieve mood logs for session       |
| `GET`  | `/api/stats`         | Aggregate chatbot statistics         |
| `POST` | `/api/feedback`      | Submit user satisfaction rating      |

### Example — Send a Message

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "I feel very overwhelmed and stressed lately"
  }'
```

---

## 🛡️ Crisis Safety & Helplines

Safety is paramount. Messages with potential self-harm indicators trigger instant crisis intervention responses with verified helplines:

- 🇲🇦 **Morocco:** **15** or **3114**
- 🇺🇸 **US:** **988**
- 🌍 **International:** [befrienders.org](https://www.befrienders.org)

---

## 🧪 Testing

Run the full end-to-end test suite to verify crisis detection, intent classification, multilingual routing, and LLM response generation:

```bash
python test_pipeline.py
```

---

## ⚠️ Disclaimer

**BMA is an educational support tool and is not a substitute for professional clinical medical advice or diagnosis.**
If you or someone you know is in immediate danger, please reach out to emergency services or a healthcare professional immediately.

---

*BMA v1.0.0 · MIT License · Created with ❤️ by Bilal Jellaoui, Mohammed Azil, and Ayoube Echihami*
