import json 
import google.generativeai as genai
from backend.conf import GEMINI_API_KEY
from backend.agents.planner import safe_generate

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

def execute_task(task: str):
    prompt = f"""
You are an expert developer assistant.

Break this task into executable steps. 

Rules:
- Give commands if applicable 
- Be specific
- Max 5 steps 
- No explanations 
- Output STRICT JSON only

Task = {task}

Format:
{{
    "task": "...",
    "steps": ["...", "...", "..."]
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