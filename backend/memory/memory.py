import json 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "data.json")

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)