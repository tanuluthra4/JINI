from backend.conf import ASSISTANT_NAME
from backend.db import get_db_connection
from backend.helper import speak, remove_words
from backend.input.speech import takecommand
import pywhatkit as kit
import subprocess, datetime

conn, cursor = get_db_connection()

def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        if results:
            phone = str(results[0])

            if not phone.startswith('+91'):
                phone = '+91' + phone

            return phone, query

        else:
            speak("Contact not found")
            return 0, 0
        
    except Exception as e:
        speak('Error accessing contacts')
        print(e)
        return 0, 0
    

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
            now = datetime.datetime.now()
            kit.sendwhatmsg_instantly(phone, message)
            speak("message send successfully to "+name)
            return True 
        
        elif "video call" in query: 
            speak("Starting video call with" + name)
            whatsapp_url = f"whatsapp://video?phone={phone}"
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
            return True 
        
        elif "call" in query:
            speak("Calling" + name + "on WhatsApp")
            whatsapp_url = f"whatsapp://call?phone={phone}"
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
            return True 
        
        else:
            speak("I didn't understand the communication request.")
            return False 
        
    except Exception as e:
        print(f"[COMMUNICATION_HANDLER ERROR]: {e}")
        speak("Something went wrong while communicating")
        return False 
    