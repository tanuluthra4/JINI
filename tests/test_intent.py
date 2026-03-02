from backend.intent import classify_intent

def test_system_intent():
    intent, _ = classify_intent("start chrome")
    assert intent == "SYSTEM"

def test_communication_intent():
    intent, _ = classify_intent("video call mom")
    assert intent == "COMMUNICATION"

def test_media_intent():
    intent, _ = classify_intent("play music")
    assert intent == "MEDIA"

def test_ai_fallback():
    intent, _ = classify_intent("what is quantum computing?")
    assert intent == "AI"

def test_mixed_query_priority():
    intent, _ = classify_intent("open youtube and play music")
    # define expected behavior clearly 
    assert intent == "SYSTEM"

def test_uppercase_input():
    intent, _ = classify_intent("START CHROME")
    assert intent == "SYSTEM"

def test_extra_spaces():
    intent, _ = classify_intent("   play    music   ")
    assert intent == "MEDIA"

def test_empty_string():
    intent, _ = classify_intent("")
    assert intent == "AI"