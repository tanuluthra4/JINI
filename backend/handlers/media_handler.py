from backend.helper import speak
from backend.feature import PlayYoutube

def play_media(query: str) -> bool:
    '''
    Handles media-related commands such as:
    - Playing YouTube videos 
    - Playing songs 
    Returns True if media was played, else False 
    '''
    try: 
        if "youtube" in query or "play" in query:
            PlayYoutube(query)
            return True 
        
        speak("I couldn't find any media to play.")
        return False 
    
    except Exception as e: 
        print(f"[MEDIA_HANDLER ERROR]: {e}")
        speak("Something went wrong while playing media.")
        return False 