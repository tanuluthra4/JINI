import speech_recognition as sr
import eel
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