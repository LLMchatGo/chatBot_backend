import speech_recognition as sr
from gtts import gTTS
import os   
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import Agent

class CallAgent:
    def __init__(self, user_data_path="userdata.txt"):
        self.agent = Agent()

        with open(user_data_path, "r") as f:
            self.user_data = f.read()

        self.recognizer = sr.Recognizer()

    def listen(self):
        print("🎤 Listening... (speak now)")
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech Recognition error: {e}")
            return None

    def speak(self, text):
        print(f"🧠 Bot says: {text}")
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        os.system("start response.mp3" if os.name == "nt" else "afplay response.mp3")

    def run(self):
        print("📞 Call Agent Activated. Say 'exit' to stop.")
        while True:
            user_input = self.listen()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Ending call session.")
                break

            try:
                result = self.agent.classify_query(user_input, self.user_data)
                print("DEBUG: Agent result:", result)
                bot_reply = result.get("response")
                if not bot_reply and "tool_result" in result and "output" in result["tool_result"]:
                    bot_reply = result["tool_result"]["output"]
                if not bot_reply:
                    bot_reply = "Sorry, something went wrong."
            except Exception as e:
                print("ERROR:", e)
                bot_reply = "Sorry, something went wrong."

            self.speak(bot_reply)

if __name__ == "__main__":
    agent = CallAgent()
    agent.run()
