import requests
import google.generativeai as genai
from backend.conf import GEMINI_API_KEY

def get_repo_info(repo_url):
    try:
        # Extract owner and repo name from the URL
        parts = repo_url.rstrip('/').split('/')

        if len(parts) < 5 or parts[-3] != "github.com":
            return {"error": "Invalid GitHub repository URL."}
        owner = parts[-2]
        repo = parts[-1]

        # GitHub API endpoint for repository information
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        # Make a GET request to the GitHub API
        response = requests.get(api_url)

        if response.status_code == 200:
            repo_info = response.json()
            return {
                "name": repo_info.get("name"),
                "description": repo_info.get("description"),
                "stars": repo_info.get("stargazers_count"),
                "forks": repo_info.get("forks_count"),
                "language": repo_info.get("language"),
                "url": repo_info.get("html_url")
            }
        else:
            return {"error": f"Failed to fetch repository info. Status code: {response.status_code}"}
        
    except Exception as e:
        return {"error": str(e)}
    
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

def analyze_repo(repo_data):
    prompt = f"""
You are a strict senior engineer reviewing a GitHub project.

Repository:
Name: {repo_data['name']}
Description: {repo_data['description']}
Language: {repo_data['language']}

Give a DEVELOPER-LEVEL review:

1. 3 SPECIFIC technical weaknesses (architecture, scalability, design issues)
2. 3 ACTIONABLE improvements (what exactly to change/add)
3. 2 MISSING features that would make it production-ready
4. 1 HIGH-IMPACT suggestion that would make this project stand out

Rules:
- NO generic advice
- NO explanations like "Python is good"
- Be direct, critical, and specific
- Assume this is a student project that needs to reach internship level
"""
    try:
        response = model.generate_content(prompt)
        return {"analysis": response.text}
    except Exception as e:
        return {"error": str(e)}