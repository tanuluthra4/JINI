import os
from shlex import quote
import struct 
import subprocess
import time 
import webbrowser
from hugchat import hugchat
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
from backend.conf import ASSISTANT_NAME, GEMINI_API_KEY, PICOVOICE_ACCESS_KEY
import google.generativeai as genai
import sqlite3
from backend.db import get_db_connection
from backend.helper import extract_yt_term, remove_words, speak

conn, cursor = get_db_connection()

def OpenCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute( 
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    try:
        kit.playonyt(search_term)
    except Exception as e:
        print("Error playing YouTube:", e)
        speak("Having trouble playing on YouTube. Opening in browser instead.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")

"""
Wake-word detection using Picovoice Porcupine.
Currently not enabled in the main execution flow.
Planned for future hands-free activation of JINI.
"""
def hotword():
    access_key=PICOVOICE_ACCESS_KEY
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(access_key=access_key,keywords=["alexa","jarvis"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")
                speak("Yes, how can I help you?")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
    
def whatsApp(Phone, message, flag, name):
    import datetime

    try:
        if flag == 'message':
            now = datetime.datetime.now()
            kit.sendwhatmsg_instantly(Phone, message)
            jini_message = "message send successfully to "+name

        elif flag == 'call':
            jini_message = "Calling" + name + "on WhatsApp"
            whatsapp_url = f"whatsapp://call?phone={Phone}"
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)

        elif flag == 'video call':
                jini_message = "Starting video call with" + name
                whatsapp_url = f"whatsapp://video?phone={Phone}"
                subprocess.run(f'start "" "{whatsapp_url}"', shell=True)

        else:
            jini_message = "Sorry, I couldn't understand the type of whatsapp action"

    except Exception as e:
        print("Whatsapp error: ", e)
        jini_message = "Sorry, I couldn't complete your whatsapp action"
        
    speak(jini_message)


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