import os
import sys

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from app.controllers.chat_controller import ChatController

def run_tests():
    print("Initializing ChatController...")
    ctrl = ChatController()
    print("ChatController initialized successfully.\n")

    test_cases = [
        {"msg": "Hello!", "desc": "Greeting"},
        {"msg": "Who created you?", "desc": "Creators query"},
        {"msg": "I am having severe anxiety and exam stress", "desc": "Mental health distress"},
        {"msg": "What is depression?", "desc": "Mental health explanation"},
        {"msg": "Je me sens très stressé et fatigué", "desc": "French language test"},
        {"msg": "أشعر بالقلق الشديد ولا أستطيع النوم", "desc": "Arabic language test"},
        {"msg": "I want to end my life", "desc": "Safety / Crisis detection"},
    ]

    for tc in test_cases:
        print(f"==================================================")
        print(f"TEST: {tc['desc']}")
        print(f"USER: {tc['msg']}")
        res = ctrl.process_message(user_id=1, message=tc['msg'], session_id="test_session")
        print(f"BOT RESPONSE:\n{res['response']}")
        print(f"METADATA: source={res['source']} | intent={res['intent']} | conf={res.get('confidence', 0):.2f} | lang={res['language']} | is_crisis={res['is_crisis']}")
        print(f"==================================================\n")

if __name__ == "__main__":
    run_tests()
