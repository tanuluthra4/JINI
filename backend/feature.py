from hugchat import hugchat
from backend.conf import GEMINI_API_KEY
import google.generativeai as genai
from backend.agents.planner import generate_plan
from backend.agents.executor import execute_task
from backend.memory.memory import save_memory, load_memory
import re

def chatBot(query):
    user_input = query.lower()
    response_text = ""

    if "github.com" in user_input:
        from backend.tools.github_tool import get_repo_info, analyze_repo

        match = re.search(r'(https?://github\.com/\S+)', query)
        if not match:
            return "Please provide a valid GitHub repository URL."
        
        repo_url = match.group(1)
        repo_info = get_repo_info(repo_url)

        if "error" not in repo_info:
            analysis = analyze_repo(repo_info)
            if "error" not in analysis:
                response_text += f"Repository Analysis:\n{analysis['analysis']}\n"
            else:
                print(f"Analysis Error: {analysis['error']}")
                response_text += "Sorry, I couldn't analyze the repository.\n"
        else:
            print(f"Repo Info Error: {repo_info['error']}")
            response_text += "Sorry, I couldn't fetch the repository information.\n"

        return response_text

    if "done" in user_input:
        memory = load_memory()

        try:
            task_num = int(user_input.split()[-1]) - 1
            memory["tasks"][task_num]["done"] = True
            save_memory(memory)
            return f"Task {task_num+1} marked as completed."
        except:
            return "Invalid task number."

    if "continue" in user_input or "next" in user_input:
            memory = load_memory()

            if isinstance(memory, dict) and "tasks" in memory:
                response_text = f"Continuing: {memory['goal']}\n\n"

                for idx, item in enumerate(memory["tasks"]):
                    if not item["done"]:
                        response_text += f"Task {idx+1}: {item['task']}\n"

                return response_text
            else:
                return "No previous plan found. Please ask for a new plan first.\n"

    trigger_words = ["build", "create", "prepare", "learn", "make"]

    if any(word in user_input for word in trigger_words):
        plan = generate_plan(query)

        if isinstance(plan, dict) and "tasks" in plan:
            structured_tasks = [{"task": t, "done": False} for t in plan["tasks"]]

            save_memory({
                "goal": plan["goal"],
                "tasks": structured_tasks
            })
        
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