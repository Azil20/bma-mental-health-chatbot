"""
test_chat.py - Unit & integration tests for the chat controller
"""

import unittest
from app.controllers.chat_controller import ChatController

class TestChat(unittest.TestCase):
    def setUp(self):
        self.controller = ChatController()

    def test_crisis_detection(self):
        resp = self.controller.process_message(1, "I want to kill myself")
        self.assertIn("15", resp)  # crisis helpline expected

    def test_normal_intent(self):
        resp = self.controller.process_message(1, "Hello")
        self.assertIsNotNone(resp)

if __name__ == '__main__':
    unittest.main()