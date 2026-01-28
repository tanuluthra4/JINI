from backend.conf import ASSISTANT_NAME
from backend.db import get_db_connection
from backend.helper import speak
import os
import webbrowser

def open_application(query: str) -> bool:
    '''
    Opens a system or web application based on user query.
    Returns True if something was opened, else False.
    '''

    cleaned_query = (
        query.lower()
        .replace(ASSISTANT_NAME.lower(), "")
        .replace("open", "")
        .strip()
    )

    if not cleaned_query:
        speak("Please tell me what to open.")
        return False

    conn, cursor = get_db_connection()

    try: 
        # 1. Check system commands
        cursor.execute(
            "SELECT path FROM sys_command WHERE name = ?",
            (cleaned_query,)
        )
        result = cursor.fetchone()

        if result:
            speak(f"Opening {cleaned_query}")
            os.startfile(result[0])
            return True 
        
        # 2. Check web commands 
        cursor.execute(
            "SELECT url FROM web_command WHERE name = ?",
            (cleaned_query,)
        )
        result = cursor.fetchone()

        if result:
            speak(f"Opening {cleaned_query}")
            webbrowser.open(result[0])
            return True
        
        # 3. Fallback: OS command 
        speak(f"Trying to open {cleaned_query}")
        os.system(f"start {cleaned_query}")
        return True
    
    except Exception as e:
        print(f"[SYSTEM_HANDLER ERROR]: {e}")
        speak("I couldn't open that")
        return False 
    
    finally:
        conn.close()