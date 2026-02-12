import eel
import time
import logging
from backend.command import get_ai_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_routes():
    @eel.expose
    def ask_ai(prompt):
        try:
            time.sleep(0.2)
            return get_ai_response(prompt)
        except Exception as e:
            logger.error("AI error occurred", exc_info=True)
            return "Sorry, I couldn't connect to backend right now."

    @eel.expose
    def navigate_to(page):
        try:
            eel.start(page, mode="edge", size=(1000, 700), block=True)
        except Exception as e:
            logger.error("Navigation error occurred", exc_info=True)


def start_app():
    eel.init("frontend")
    register_routes()
    logger.info("🚀 Launching JINI interface...")
    eel.start("pages/index.html", mode="edge", size=(1000, 700), block=True)


if __name__ == "__main__":
    logger.info("🧠 JINI is starting up...")
    start_app()