import google.generativeai as genai
import os
from speak import Speaker
from dotenv import load_dotenv

load_dotenv()
speaker = Speaker()

system_prompt = """
You are IqraBot, a helpful and intelligent virtual assistant designed for students, staff, and faculty at Iqra University (IU).
You speak politely, respond with clear and informative answers, and can assist with academic, technical, and general questions.
Greet users, ask how you can help, and maintain a professional yet friendly tone.
"""
API_KEY = os.getenv("GEMINI_API_KEY")

class Chatbot:
    def __init__(self):
        # Initialize the chatbot
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-8b",
            system_instruction=system_prompt
        )
        self.chat = model.start_chat(history=[])
        print("🎓 IqraBot: Assalamu Alaikum! I'm IqraBot – your smart assistant at Iqra University.")
        print("🎓 IqraBot: How can I help you today? Type 'exit' to end the chat.\n")
        self.respond("Greet the user and ask how you can help.")

    def respond(self, user_input):
        if user_input.strip() == "":
            return
        # Exit condition
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🎓 IqraBot: Allah Hafiz! Wishing you success at Iqra University.")
            os._exit(0)
        try:
            response = self.chat.send_message(user_input)
            output = response.text.strip()
            speaker.speak(output)
            print("🎓 IqraBot:", output)
            # Show token usage if available
            if hasattr(response, "usage_metadata"):
                tokens_used = response.usage_metadata.total_token_count
                print(f"🔢 Tokens used in this interaction: {tokens_used}")
        except Exception as e:
            print("⚠️ Error communicating with Gemini API:", e)
