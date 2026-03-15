from dataclasses import dataclass
from typing import Dict

@dataclass
class IntentResult:
    intent: str
    entities: Dict[str, str]
    raw_query: str