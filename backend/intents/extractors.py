import re 

def extract_city(query: str):

    match = re.search(r"in ([a-zA-Z]+)", query)

    if match:
        return match.group(1).lower()

    return None