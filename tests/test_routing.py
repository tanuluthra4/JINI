from backend.command import route_query

def test_weather_route():
    response = route_query("weather in delhi")
    assert "weather" in response.lower()