import google.generativeai as genai
from backend.conf import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def explain_problem(problem):

    model = genai.GenerativeModel("models/gemini-2.5-flash")

    prompt = f"""
You are a FAANG coding interviewer.

Problem:
{problem}

Give response in this format:

1. Problem Understanding

2. Brute Force Approach

3. Optimal Approach

4. Step-by-Step Logic

5. Time and Space Complexity

6. Common Interview Mistakes

7. Implementation Strategy

Keep response concise and practical.
"""

    response = model.generate_content(prompt)

    return response.text