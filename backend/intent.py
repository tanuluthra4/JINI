from backend.models import IntentResult

def extract_city(query: str):
    words = query.lower().split()
    if "in" in words:
        idx = words.index("in")
        if idx + 1 < len(words):
            return words[idx + 1]
    return None

def classify_intent(query: str):
    query = query.lower().strip()

    system_keywords = {"open", "launch", "start"}
    communication_keywords = {"message", "call", "video call", "whatsapp"}
    media_keywords = {"play", "youtube"}
    weather_keywords = {"weather", "temperature", "forecast"}

    words = set(query.split())

    if words & system_keywords:
        return IntentResult(
            intent="SYSTEM",
            entities={},
            raw_query=query
        )
        
    if words & communication_keywords:
        return IntentResult(
            intent="COMMUNICATION",
            entities={},
            raw_query=query
        )
        
    if words & media_keywords:
        return IntentResult(
            intent="MEDIA",
            entities={},
            raw_query=query
        )
    
    if words & weather_keywords:
        city = extract_city(query)
        return IntentResult(
            intent="WEATHER",
            entities={"city": city} if city else {},
            raw_query=query
        )
        
    return IntentResult(
            intent="AI",
            entities={},
            raw_query=query
        )