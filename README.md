# JINI – AI-Based Voice-Controlled Desktop Assistant    

JINI is a voice-enabled AI desktop assistant that integrates real-time system automation with conversational AI.  
It supports both command-based voice control and text-based AI interaction through a structured, safety-first architecture.   

Unlike typical chatbot projects, JINI separates system-level command execution from AI-driven conversation, ensuring reliable automation without unintended actions.   
The assistant maintains persistent conversational memory across sessions and supports multimodal interaction via a web-based interface.      

## Key Features

- 🎤 Voice-controlled desktop commands
- 💬 Text-based conversational chatbot
- 🗣️ Text-to-speech responses
- 🧠 AI-powered responses using Gemini API
- 🖥️ Application launching and system automation
- 📁 Local database for contacts and system commands
- 🌐 Web-based user interface
- 🔐 Environment-based API key handling

## Persistent Memory Model

JINI maintains client-side conversational memory using a unified storage mechanism.  
Both text-based chat (index.html) and voice-based interaction (mic.html) read from and write to the same memory store.  

- Conversation history is persisted across reloads  
- Messages are timestamped and rendered in chronological order  
- Memory can be cleared explicitly by the user   
- Ensures continuity between voice and text interactions    

This design makes JINI behave like a single, consistent assistant rather than separate interaction modes.  

## System Architecture Overview

JINI uses two independent input pipelines, intentionally designed to handle different interaction types.

1. Text Input Pipeline (Chatbot Mode)
Text input is processed exclusively through the Gemini AI model.
Purpose:
- General conversation
- Knowledge-based queries
- AI assistance
Flow:
Text Input → Gemini AI → Text Response → Voice Output
Text input does not trigger system commands to avoid ambiguity and unintended execution.

2. Voice Input Pipeline (Command Mode)
Voice input is command-oriented and therefore classified before execution.
Purpose:
- Open applications
- Play media (YouTube, songs)
- Call or message stored contacts
- Perform system-level actions
Flow:
Voice Input
 → Speech-to-Text
 → Command Classification
```text
    ├─ System Command → Local Execution
    └─ General Query → Gemini AI 
```
This separation ensures accuracy, security, and reliability in system control.

## Project Structure

```text
JINI/
│
├── backend/
│   ├── command.py        # Command interpretation and routing
│   ├── feature.py        # System-level features and actions
│   ├── helper.py         # Utility and helper functions
│   ├── conf.py           # Configuration (API keys, assistant name)
│   └── db.py             # Database setup and access
│
├── frontend/
│   ├── html/
│   │   ├── index.html     # Chatbot interface
│   │   └── mic.html       # Voice interaction UI
│   │
│   ├── css/
│   │   ├── main.css       # Chatbot UI styles
│   │   └── mic.css        # Mic UI styles
│   ├── js/
│   │   ├── app.js         # Chatbot logic + memory handling
│   │   └── mic.js         # Microphone input + audio visualization
│   │
│   └── assets/
│       └── favicon.png    # JINI application icon
│
├── main.py               # Application entry point
├── jini.db               # SQLite database (generated locally)
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
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

## Wake Word Detection (Planned)

The system includes preliminary implementation for wake-word detection using Picovoice Porcupine.
This feature is currently disabled in the final build to avoid continuous microphone usage and system overhead.
It is planned to be enabled in future versions for hands-free interaction.

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
PICOVOICE_API_KEY=your_api_key
ASSISTANT_NAME=JINI

5. Run Application
python main.py

## Design Decisions

- Text and voice inputs are intentionally separated
- Voice commands are classified before execution
- Text input is restricted to AI responses only
- Local database ensures fast access and offline capability
- Modular backend improves maintainability and scalability

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