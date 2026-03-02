def classify_intent(query: str):
    query = query.lower().strip()

    system_keywords = {"open", "launch", "start"}
    communication_keywords = {"message", "call", "video call", "whatsapp"}
    media_keywords = {"play", "youtube"}

    words = set(query.split())

    if words & system_keywords:
        return "SYSTEM", query
        
    if words & communication_keywords:
        return "COMMUNICATION", query
        
    if words & media_keywords:
        return "MEDIA", query
        
    return "AI", query