from hugchat import hugchat
from backend.conf import GEMINI_API_KEY
import google.generativeai as genai
from backend.agents.planner import generate_plan
from backend.agents.executor import execute_task

def chatBot(query):
    user_input = query.lower()
    response_text = ""

    trigger_words = ["build", "create", "prepare", "learn", "make"]

    if any(word in user_input for word in trigger_words):
        plan = generate_plan(query)
        
        if isinstance(plan, dict) and "error" not in plan:
            response_text += f"Here's the plan to achieve your goal: {plan['goal']}\n\n"
            for idx, task in enumerate(plan['tasks']):
                response_text += f"Task {idx+1}: {task}\n"

            # Only execute FIRST task (controlled)
            if "how" in user_input or "execute" in user_input:
                first_task = plan['tasks'][0]
                execution = execute_task(first_task)

                if isinstance(execution, dict) and "error" not in execution:
                    response_text += "\n🔧 First Task Breakdown:\n"
                    for step in execution['steps']:
                        response_text += f" - {step}\n"
                else:
                    response_text += "\nCouldn't break down the first task.\n"

    try: #Try using Gemini first 
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        if response_text == "":
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