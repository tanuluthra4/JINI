import pyttsx3
import speech_recognition as sr
import eel
from backend import feature
from backend.helper import speak

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        eel.DisplayMessage("Listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=8)

    try:
        print("Recognizing....")
        eel.DisplayMessage("Listening....")
        query = r.recognize_google(audio, language='en-US')
        print(F"User said: {query}\n")
        eel.DisplayMessage(query)
        return query.lower()

    except Exception as e:
        print(f"Error : {e}")
        print("Sorry, I didn't catch that")
        speak("Sorry, I didn't catch that")
        return None

@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()
        if not query:
            return
        print(query)
        eel.senderText(query)

    else:
        query = message.lower().strip()
        print(f"Message received: {query}")
        eel.senderText(query)

    try:
        if query:
            if "open" in query:
                feature.OpenCommand(query)
            elif "message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            elif "on youtube" in query or "play" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            else:
                from backend.feature import chatBot
                response = chatBot(query)
                if response:
                    speak(response)
                    eel.DisplayMessage(response)
                else:
                    speak("I’m here, but didn’t get that.")
        else:   
            speak("No command was given.")

    except Exception as e:
        print(f"An error occurred: {e}")
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