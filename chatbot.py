from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
from speak import Speaker
from dotenv import load_dotenv

load_dotenv()
speaker = Speaker()
model_id = "gemini-1.5-flash"

google_search_tool = Tool(
    google_search_retrieval = GoogleSearch()
)

system_prompt = """
You are IqraBot, a helpful and intelligent virtual assistant designed for students, staff, and faculty at Iqra University (IU).
You speak politely, respond with clear and informative answers, and can assist with academic, technical, and general questions.
Greet users, ask how you can help, and maintain a professional yet friendly tone.
Answer as briefly as possible.
access information from: https://iqra.edu.pk/
You can also use the Google Search tool to find information not in your training data.
return the response in without any formatting.
"""

API_KEY = os.getenv("GEMINI_API_KEY")

class Chatbot:
    def __init__(self):
        # Initialize the chatbot
        self.client = genai.Client(api_key=API_KEY)
        # self.respond("Greet the user and ask how you can help.")
        self.respond("What Courses does iqra university offer for Masters in Main Campus.")

    def respond(self, user_input, mic_stream=None):
        if user_input.strip() == "":
            return
        # Exit condition
        if user_input.lower() in ["exit", "quit", "bye"]:
            # print("🎓 IqraBot: Allah Hafiz! Wishing you success at Iqra University.")
            os._exit(0)
        try:
            responses = self.client.models.generate_content(
                model=model_id,
                config=GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[google_search_tool],
                    response_modalities=["TEXT"],
                ),
                contents=user_input
            )
            for each in responses.candidates[0].content.parts:
                print(each.text)
            print(responses.candidates[0].grounding_metadata.search_entry_point.rendered_content)
            response = [each.text for each in responses.candidates[0].content.parts]
            response = ''.join(response)
            output = response.strip().replace("*", " ")
            print("🎓 IqraBot:", output)
            if mic_stream:
                mic_stream.pause()
            speaker.speak(output)
            if mic_stream:
                mic_stream.resume()
            # Show token usage if available
            if hasattr(response, "usage_metadata"):
                tokens_used = response.usage_metadata.total_token_count
                print(f"🔢 Tokens used in this interaction: {tokens_used}")
        except Exception as e:
            print("⚠️ Error communicating with Gemini API:", e)
chatbot = Chatbot()