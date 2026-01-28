import pyttsx3
import speech_recognition as sr
import eel
from backend.feature import chatBot
from backend.helper import speak
from backend.handlers.system_handler import open_application
from backend.handlers.communication_handler import handle_communication 
from backend.handlers.media_handler import play_media 
from backend.intent import classify_intent
from backend.input.speech import takecommand

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
        if intent == "SYSTEM":
            open_application(query)

        elif intent == "COMMUNICATION":
            handle_communication(query)

        elif intent == "MEDIA":
            play_media(query)

        else: # AI fallback
            response = chatBot(query)
            if response:
                speak(response)
                eel.DisplayMessage(response)
            else:
                speak("I'm here, but didn't get that")

    except Exception as e:
        print(f"Error while processing command: {e}")
        speak("Sorry, something went wrong.")
    
    eel.ShowHood()

@eel.expose
def get_ai_response(message):
    from backend.feature import chatBot
    try:
        response = chatBot(message)
        if response is None:
            return "I am listening...."
        return response 
    except Exception as e:
        print(f"Error : {e}")
        return "Sorry, I couldn't process that right now"

@eel.expose
def mic_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        eel.showResponse(f"🗣️ You said: {text}")

        if any(word in text.lower() for word in ["open", "call", "message", "video", "youtube", "play"]):
            takeAllCommands(text)  # Executes feature actions directly
            return
        
        # Get AI response
        response = get_ai_response(text)
        print("🤖 JINI:", response)

        # Send to frontend
        eel.showResponse(response)

        # Speak it
        speak(response)

    except sr.UnknownValueError:
        print("Could not understand audio")
        eel.showResponse("Sorry, I didn’t catch that.")
    except sr.RequestError:
        print("Speech service error")
        eel.showResponse("Speech recognition service not available.")