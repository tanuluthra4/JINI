def handle_weather(query: str):
    city = query.entities.get("city")
    if city:
        return f"fetching weather for {city}"
    return "Please specify a city"