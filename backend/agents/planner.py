import json
import google.generativeai as genai
from backend.conf import GEMINI_API_KEY
import time 

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

def safe_generate(prompt):
    for _ in range(3):
        try:
            return model.generate_content(prompt).text.strip()
        except Exception as e:
            if "429" in str(e):
                time.sleep(2)  # Wait before retrying
            else:
                print(f"Error generating content: {e}")
        
    return "Sorry, I'm having trouble generating a response right now."

def generate_plan(user_goal: str):
    prompt = f"""
You are an autonomous developer copilot.

Convert the given goal into a HIGHLY ACTIONABLE execution plan.

Rules:
- Max 7 steps
- Each step must involve a clear action + tool/platform
- Avoid generic advice
- Be specific about which tools to use (React, Python, GitHub, LeetCode, Vercel, etc.)
- No explanations, just the plan
- Output STRICT JSON only 

Goal: {user_goal}

Output format: 
{{
"goal": "...",
"tasks": ["...", "..."]
}}
"""
    
    text = safe_generate(prompt).strip()
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        json_text = text[start:end]
        return json.loads(json_text)
    except:
        return {"error": "INVALID JSON", "raw": text}
    