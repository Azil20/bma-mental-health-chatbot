"""
app/services/emotion_detector.py
Emotion classification using fine-tuned DistilBERT
"""

import pickle
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

from config.config import Config
from app.utils.text_cleaner import clean_text


class EmotionDetector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.label_encoder = None

        self._load_model()

    def _load_model(self):
        """
        Load the fine-tuned DistilBERT emotion model and label encoder.
        """

        model_dir = Config.EMOTION_MODEL_DIR
        encoder_path = Config.EMOTION_ENCODER_PATH

        if not model_dir.exists():
            raise RuntimeError(f"Emotion model directory not found: {model_dir}")

        if not encoder_path.exists():
            raise RuntimeError(f"Emotion label encoder not found: {encoder_path}")

        self.tokenizer = DistilBertTokenizer.from_pretrained(str(model_dir))

        self.model = DistilBertForSequenceClassification.from_pretrained(
            str(model_dir)
        ).to(self.device)

        self.model.eval()

        with open(encoder_path, "rb") as file:
            self.label_encoder = pickle.load(file)

    def predict(self, text: str) -> dict:
        """
        Predict the emotion of a given text.

        Returns:
            {
                "emotion": str,
                "confidence": float
            }
        """

        if not text or not text.strip():
            return {
                "emotion": "neutral",
                "confidence": 0.0
            }

        cleaned_text = clean_text(text)

        inputs = self.tokenizer(
            cleaned_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=64
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)[0]

            predicted_index = torch.argmax(probabilities).item()
            confidence = probabilities[predicted_index].item()

            if hasattr(self.label_encoder, 'inverse_transform'):
                emotion = self.label_encoder.inverse_transform([predicted_index])[0]
            else:
                emotion = self.label_encoder[predicted_index]

        return {
            "emotion": emotion,
            "confidence": float(confidence)
        }