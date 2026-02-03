# JINI – AI-Based Voice-Controlled Desktop Assistant    

JINI is a voice-enabled AI desktop assistant that integrates real-time system automation with conversational AI.  
It supports both command-based voice control and text-based AI interaction through a structured, safety-first architecture.   

Unlike typical chatbot projects, JINI separates system-level command execution from AI-driven conversation, ensuring reliable automation without unintended actions.   
The assistant maintains persistent conversational memory across sessions and supports multimodal interaction via a web-based interface.      

## Key Features

- 🎤 Voice-controlled desktop commands – Open apps, launch URLs, send messages, make calls
- 💬 Text-based conversational AI – Handles queries, knowledge retrieval, and casual conversation
- 🗣️ Text-to-speech responses – Unified voice output for both AI and system responses
- 🧠 AI-powered responses – Gemini API primary, HugChat fallback for resilience
- 🖥️ System automation – Launch apps, play media, WhatsApp communication
- 📁 Local SQLite database – Stores contacts and system commands safely
- 🌐 Web-based frontend – Supports text input (index.html) and voice input (mic.html)
- 🔐 Environment-based API key handling – No sensitive data committed

## Persistent Memory Model

JINI maintains unified conversational memory across both text and voice interactions:

- Shared storage: All messages, from both index.html and mic.html, are persisted in the same memory store
- Chronological history: Messages are timestamped and displayed in order
- Reload continuity: Conversation persists across page reloads and app restarts
- Explicit clearing: Users can clear memory manually
- Safety-first separation: Voice commands trigger handlers, but text inputs never execute system-level actions

This ensures JINI behaves as one consistent assistant, not two separate interfaces.

## AI vs Command Handling 

1. Voice Commands (Command Mode):

- Classified first using intent.py
- Routed to appropriate handler:
- SYSTEM: system_handler.py → Opens apps, launches URLs
- COMMUNICATION: communication_handler.py → WhatsApp messages, calls, video calls
- MEDIA: media_handler.py → YouTube/media playback

2. Text Inputs (Chatbot Mode):

- Handled only by feature.py
- Uses Gemini API → HugChat fallback
- No system command execution to ensure security

3. Design Decision:
Voice commands and AI queries are intentionally separated to prevent accidental system actions and maintain reliability.

## System Architecture Overview

JINI uses two independent input pipelines, intentionally designed to handle different interaction types.

1. Text Input Pipeline (Chatbot Mode)
Handles text-based interaction exclusively through AI. This pipeline does not trigger system commands, ensuring safe responses.
Purpose:
- General conversation
- Knowledge-based queries
- AI assistance
Flow:
Text Input → feature.py (Gemini AI + HugChat fallback) → Voice & Text Output
Text input does not trigger system commands to avoid ambiguity and unintended execution.

2. Voice Input Pipeline (Command Mode)
Voice input is command-oriented and therefore classified before execution.
Purpose:
- Open applications
- Play media (YouTube, songs)
- Call or message stored contacts
- Perform system-level actions
Flow:
```text
    Microphone Input
        ↓
    Speech-to-Text (input/speech.py)
        ↓
    Intent Classification (intent.py)
        ├─ SYSTEM → system_handler.py → Open apps / URLs
        ├─ COMMUNICATION → communication_handler.py → WhatsApp / Calls / Messages
        ├─ MEDIA → media_handler.py → YouTube / Media Playback
        └─ AI → feature.py → Conversational AI
        ↓
    Text-to-Speech Output (helper.py)
```
This separation ensures accuracy, security, and reliability in system control.

## Project Structure

```text
JINI/
│
├── backend/
│   ├── command.py                    # Command router (routes input to correct handler)
│   ├── feature.py                    # AI chatbot only (Gemini + HugChat fallback)
│   ├── helper.py                     # Utility functions (speak, extract words, etc.)
│   ├── conf.py                       # Configuration (API keys, assistant name)
│   ├── db.py                         # Database setup and access
│   ├── intent.py                     # Input classification: SYSTEM, COMMUNICATION, MEDIA, AI
│   ├── handlers/
│   │   ├── system_handler.py         # System commands (open apps, launch URLs)
│   │   ├── communication_handler.py  # WhatsApp, calls, messages
│   │   └── media_handler.py          # YouTube/media playback
│   └── input/
│       └── speech.py                 # Speech-to-text logic
│
├── frontend/
│   ├── html/
│   │   ├── index.html                 # Chatbot interface (text input)
│   │   └── mic.html                   # Voice interaction UI
│   ├── css/
│   │   ├── main.css                   # Chatbot UI styles
│   │   └── mic.css                    # Mic UI styles
│   ├── js/
│   │   ├── app.js                     # Chatbot logic + memory handling
│   │   └── mic.js                     # Microphone input + audio visualization
│   └── assets/
│       └── favicon.png                # JINI application icon
│
├── main.py                             # Application entry point (launches Eel UI)
├── jini.db                             # SQLite database (generated locally)
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (not committed)
├── .gitignore
└── README.md
```

## Database Design

The project uses SQLite for lightweight local storage.
Tables
sys_command – Stores application names and executable paths/URLs
contacts – Stores contact names and phone numbers
Sensitive data is excluded from version control.

## Technologies Used

1. Backend
- Python
- SQLite
- SpeechRecognition
- Pyttsx3
- PyAutoGUI

2. Frontend
- HTML
- CSS
- JavaScript
- Eel (Python–Web bridge)

3. APIs & Tools
- Google Gemini AI
- Picovoice (Wake word detection)
- YouTube automation
- Text-to-Speech engine (SAPI5)

## Installation & Setup

1. Clone Repository  
git clone https://github.com/tanuluthra4/JINI.git  
cd JINI  

2. Create Virtual Environment   
python -m venv envjini  
envjini\Scripts\activate  

3. Install Dependencies  
pip install -r requirements.txt  

4. Configure Environment Variables  
Create a .env file:  
GEMINI_API_KEY=your_api_key
ASSISTANT_NAME=JINI  

5. Run Application   
python main.py  

## Design Decisions

- Separate input pipelines: Voice commands trigger handlers, text input goes only to AI
- Command classification: All voice commands are classified first to avoid unintended actions
- AI fallback: Text inputs handled only by feature.py ensures system safety
- Persistent memory: Unified storage across text and voice modes for consistency
- Modular backend: Handlers for system, communication, and media make code maintainable
- Local database: Ensures offline capability for contacts and system commands

These choices were made to ensure robustness, clarity, and system safety.

## Limitations

- Platform dependent (Windows-based)
- Requires internet for AI responses
- Limited to predefined system commands
- Voice recognition accuracy depends on environment noise

## Future Enhancements

- Cross-platform support
- User authentication
- Dynamic command learning
- Mobile integration
- Enhanced NLP-based command classification
- Cloud-based database synchronization

## Academic Declaration

This project is developed as part of the B.Tech Capstone Project under the Department of Computer Engineering,
J.C. Bose University of Science & Technology, YMCA, Faridabad.

## Author

Tanu Luthra  
B.Tech Computer Engineering  
J.C. Bose University of Science & Technology, YMCA  

## Demo
A short screen recording demonstrating memory persistence, voice commands, and reload recovery is included in the repository.