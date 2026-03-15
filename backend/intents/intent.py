from backend.models import IntentResult
from backend.intents.patterns import INTENT_PATTERNS
from backend.intents.extractors import extract_city

def classify_intent(query: str):
    query = query.lower().strip()
    
    for intent, patterns in INTENT_PATTERNS.items():

        for pattern in patterns:

            if pattern in query:
                entities = {}

                if intent == "WEATHER":
                    city = extract_city(query)
                    if city:
                        entities["city"] = city

                return IntentResult(
                    intent=intent,
                    entities=entities,
                    raw_query=query
                )
            
    return IntentResult(
            intent="AI",
            entities={},
            raw_query=query
        )