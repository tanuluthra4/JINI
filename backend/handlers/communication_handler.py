from backend.feature import findContact, whatsApp
from backend.helper import speak
from backend.input.speech import takecommand

def handle_communication(query: str) -> bool:
    '''
    Handle communication related commands:
    - WhatsApp message 
    - WhatsApp call
    - WhatsApp video call 
    Returns True if action executed, else False 
    '''

    try: 
        phone, name = findContact(query)

        if phone == 0:
            speak("I couldn't find the contact.")
            return False
        
        # Determine intent 
        if "message" in query:
            speak("What message should I send?")
            message = takecommand()
            if not message:
                speak("Message cancelled.")
                return False 
            
            whatsApp(phone, message, "message", name)
            return True 
        
        elif "video call" in query: 
            whatsApp(phone, "", "video call", name)
            return True 
        
        elif "call" in query:
            whatsApp(phone, "", "call", name)
            return True 
        
        else:
            speak("I didn't understand the communication request.")
            return False 
        
    except Exception as e:
        print(f"[COMMUNICATION_HANDLER ERROR]: {e}")
        speak("Something went wrong while communicating")
        return False 
    