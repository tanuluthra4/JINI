def classify_intent(query: str):
    query = query.lower().strip()

    system_keywords = ["open", "launch", "start"]
    communication_keywords = ["message", "call", "video call", "whatsapp"]
    media_keywords = ["play", "on youtube", "youtube"]

    for word in system_keywords:
        if word in query:
            return "SYSTEM", query
        
    for word in communication_keywords:
        if word in query:
            return "COMMUNICATION", query
        
    for word in media_keywords:
        if word in query:
            return "MEDIA", query
        
    return "AI", query