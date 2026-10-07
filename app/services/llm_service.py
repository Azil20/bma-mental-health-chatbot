"""
llm_service.py - LLM fallback using Google Gemini API.
With empathetic mental-health guidance and conversational intelligence.
Creators: Bilal Jellaoui, Mohammed Azil, Ayoube Echihami
"""

import logging
import requests
from config.config import Config

logger = logging.getLogger(__name__)

REDIRECT_SYSTEM_PROMPT = """You are BMA, a compassionate, empathetic AI mental health companion.
You were created by Bilal Jellaoui, Mohammed Azil, and Ayoube Echihami.

Creators Information:
- Bilal Jellaoui is from Sidi Kacem, Morocco. He is a Master's student in Big Data, Artificial Intelligence and Advanced Applications.
- Mohammed Azil is from Beni Mellal, Morocco. He is a Master's student in Big Data, Artificial Intelligence and Advanced Applications.
- Ayoube Echihami is from El Jadida, Morocco. He is a Master's student in Big Data, Artificial Intelligence and Advanced Applications.
- Together, they created BMA to provide empathetic, accessible emotional support and well-being guidance.
When asked about your creators, who made you, or your origins, share this information accurately and warmly.

Your Personality & Mission:
- You are warm, caring, supportive, non-judgmental, and a patient active listener.
- When the user shares feelings of stress, anxiety, sadness, loneliness, or burnout, validate their feelings and offer gentle, practical coping strategies (like deep breathing, mindfulness, self-compassion, grounding exercises).
- When the user greets you or checks in (e.g., "hi", "hello", "how are you"), reply warmly and ask how they are feeling today.
- When asked general questions about mental health topics (depression, anxiety, self-care, sleep, meditation), provide clear, insightful, compassionate explanations.
- If the user asks about completely unrelated topics (sports, weather, trivia, tech), answer briefly and politely pivot back to their well-being (e.g., "I don't keep up with that, but I'd love to know how you are feeling today!").
- Keep responses natural, concise (2 to 4 sentences), and supportive.
- Do not repeat generic canned phrases. Respond specifically and thoughtfully to what the user said.
"""

class LLMService:
    def __init__(self):
        self.api_key = getattr(Config, 'GEMINI_API_KEY', '') or ''
        primary_model = getattr(Config, 'LLM_MODEL_NAME', 'gemini-flash-lite-latest') or 'gemini-flash-lite-latest'
        # List of candidate models to try in case of temporary 503 / high demand spikes
        all_candidates = [primary_model, "gemini-flash-lite-latest", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.8-flash"]
        # Deduplicate while preserving order
        self.candidate_models = []
        for m in all_candidates:
            if m not in self.candidate_models:
                self.candidate_models.append(m)

        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not configured. Local fallback will be used.")
        else:
            logger.info(f"Gemini LLM initialised with primary model '{self.candidate_models[0]}'.")

    def generate_response(self, user_message: str, context: str = "") -> str:
        """Generate a response using Gemini REST API with automated model fallback."""
        if not self.api_key:
            return self._local_fallback(user_message)

        prompt_text = user_message
        if context:
            prompt_text = f"Recent conversation context:\n{context}\n\nUser: {user_message}"

        payload = {
            "system_instruction": {
                "parts": [{"text": REDIRECT_SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "parts": [{"text": prompt_text}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 350
            }
        }

        for model_name in self.candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            try:
                res = requests.post(url, json=payload, timeout=12)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            text = parts[0]["text"].strip()
                            if text:
                                logger.info(f"LLM generated response via {model_name}")
                                return text
                elif res.status_code in (503, 429, 500):
                    logger.warning(f"Model {model_name} returned {res.status_code}, trying next model...")
                    continue
                else:
                    logger.warning(f"Model {model_name} error ({res.status_code}): {res.text[:150]}")
                    continue
            except requests.exceptions.Timeout:
                logger.warning(f"Model {model_name} request timed out, trying next model...")
                continue
            except Exception as e:
                logger.warning(f"Model {model_name} call failed: {e}")
                continue

        logger.error("All Gemini candidate models failed to respond. Using local fallback.")
        return self._local_fallback(user_message)

    def _local_fallback(self, user_message: str) -> str:
        """Friendly local fallback when API is unreachable."""
        return "I'm here to support your mental well-being. How are you feeling right now, and what's on your mind?"
