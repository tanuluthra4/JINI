import eel
import time  # import time for delay
from backend.command import get_ai_response

def start():
    eel.init("frontend")

    @eel.expose
    def ask_ai(prompt):
        # Simulate thinking time
        try:
            thinking_time = 0.2  # time in seconds
            time.sleep(thinking_time)

            # Send a prompt from frontend to backend and get AI response.
            return get_ai_response(prompt)
        except Exception as e:
            print("AI error:", e)
            return "Sorry, I couldn't connect to backend right now."

    @eel.expose
    def navigate_to(page):
        # Navigate between pages inside the Eel app.
        try:
            eel.start(page, mode="edge", size=(1000, 700), block=True)
        except Exception as e:
            print("Navigation error:", e)

    print("🚀 Launching JINI interface...")
    eel.start("index.html", mode="edge", size=(1000, 700), block=True)


if __name__ == "__main__":
    print("🧠 JINI is starting up...")
    start()
