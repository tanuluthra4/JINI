from backend.intent import classify_intent

def test_system_intent():
    result = classify_intent("start chrome")
    assert result.intent == "SYSTEM"

def test_communication_intent():
    result = classify_intent("video call mom")
    assert result.intent == "COMMUNICATION"

def test_media_intent():
    result = classify_intent("play music")
    assert result.intent == "MEDIA"

def test_ai_fallback():
    result = classify_intent("what is quantum computing?")
    assert result.intent == "AI"

def test_mixed_query_priority():
    result = classify_intent("open youtube and play music")
    # define expected behavior clearly 
    assert result.intent == "SYSTEM"

def test_uppercase_input():
    result = classify_intent("START CHROME")
    assert result.intent == "SYSTEM"

def test_extra_spaces():
    result = classify_intent("   play    music   ")
    assert result.intent == "MEDIA"

def test_empty_string():
    result = classify_intent("")
    assert result.intent == "AI"

def test_weather_intent():
    result = classify_intent("weather in delhi")
    assert result.intent == "WEATHER"
    assert result.entities["city"] == "delhi"