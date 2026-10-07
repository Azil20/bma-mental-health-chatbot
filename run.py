"""
run.py - Alternative entry point for BMA Mental Health Chatbot.
Creators: Bilal Jellaoui, Mohammed Azil, Ayoube Echihami
"""
from app.routes import chat_bp
from app import create_app
from config.config import Config
from config.logging_config import setup_logging
import os

log_file = os.path.join(os.path.dirname(__file__), "logs", "app.log")
setup_logging(log_file=log_file, log_level="DEBUG" if Config.DEBUG else "INFO")

app = create_app(Config)

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
