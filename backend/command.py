import speech_recognition as sr
import eel
import logging
from backend.feature import chatBot
from backend.helper import speak
from backend.handlers.system_handler import open_application
from backend.handlers.communication_handler import handle_communication 
from backend.handlers.media_handler import play_media 
from backend.intent import classify_intent
from backend.input.speech import takecommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@eel.expose
def takeAllCommands(message=None):
    '''
    Processes user input (voice or text) and routes to the correct handler
    '''

    # Step 1: Get the query
    if message is None:
        query = takecommand()
        if not query:
            return

    else:
        query = message.lower().strip()
        
    print(f"Message received: {query}")
    eel.senderText(query)

    # Step 2: Classify intent
    intent, _ = classify_intent(query)

    # Step 3: Route Based on intent
    try:
        handlers = {
            "SYSTEM": open_application,
            "COMMUNICATION": handle_communication,
            "MEDIA": play_media
        }

        handler = handlers.get(intent)
        
        if handler: 
            handler(query)

        else: # AI fallback
            response = chatBot(query)
            if response:
                speak(response)
                eel.DisplayMessage(response)
            else:
                speak("I'm here, but didn't get that")

    except Exception as e:
        logger.error(f"Error while processing command", exc_info=True)
        speak("Sorry, something went wrong.")
    
    eel.ShowHood()

@eel.expose
def get_ai_response(message):
    try:
        response = chatBot(message)
        if response is None:
            return "I am listening...."
        return response 
    except Exception as e:
        logger.error(f"Error", exc_info=True)
        return "Sorry, I couldn't process that right now"

@eel.expose
def mic_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("🎙️ Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        logger.info(f"🗣️ You said: {text}")
        eel.showResponse(f"🗣️ You said: {text}")

        # Send everything to router 
        takeAllCommands(text)

    except sr.UnknownValueError:
        logger.error("Could not understand audio", exc_info=True)
        eel.showResponse("Sorry, I didn’t catch that.")

    except sr.RequestError:
        logger.error("Speech service error", exc_info=True)
        eel.showResponse("Speech recognition service not available.")