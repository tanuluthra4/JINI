from backend.helper import speak, extract_yt_term
import pywhatkit as kit
import webbrowser

def play_media(query: str) -> bool:
    '''
    Handles media-related commands such as:
    - Playing YouTube videos 
    - Playing songs 
    Returns True if media was played, else False 
    '''
    try: 
        if "youtube" in query or "play" in query:
            search_term = extract_yt_term(query)
            speak("Playing " + search_term + " on YouTube")
        try:
            kit.playonyt(search_term)
        except Exception as e:
            print("Error playing YouTube:", e)
            speak("Having trouble playing on YouTube. Opening in browser instead.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
            return True 
        
        speak("I couldn't find any media to play.")
        return False 
    
    except Exception as e: 
        print(f"[MEDIA_HANDLER ERROR]: {e}")
        speak("Something went wrong while playing media.")
        return False 