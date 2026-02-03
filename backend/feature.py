from hugchat import hugchat
from backend.conf import GEMINI_API_KEY
import google.generativeai as genai

def chatBot(query):
    user_input = query.lower()
    response_text = ""

    try: #Try using Gemini first 
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(user_input)
        response_text = response.text.strip()
    
    except Exception as g:
        print(f"Gemini Error {g}")

        try:
            chatbot = hugchat.ChatBot(cookie_path="backend\\cookie.json")
            id = chatbot.new_conversation()
            chatbot.change_conversation(id)
            response_text =  chatbot.chat(user_input)
        
        except Exception as h:
            response_text = "Sorry, I'm having trouble connecting right now"

    print(response_text)
    return response_text