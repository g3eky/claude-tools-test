import datetime
import requests
import json
from typing import Optional, Dict, Any

def get_current_time() -> str:
    """
    Get the current date and time.
    
    Returns:
        A string with the current date and time.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_weather(location: str, units: str = "metric") -> Dict[str, Any]:
    """
    Get the current weather for a location.
    
    Args:
        location: The city name or location
        units: The units to use (metric, imperial, standard)
        
    Returns:
        A dictionary with weather information
    """
    # This is a mock implementation
    # In a real application, you would use a weather API
    weather_data = {
        "location": location,
        "temperature": 22 if units == "metric" else 72,
        "conditions": "Sunny",
        "humidity": 65,
        "wind_speed": 10,
        "units": units,
        "timestamp": get_current_time()
    }
    
    return weather_data 


llm_tools = [
    {
        "name": "get_current_time",
        "function": get_current_time,
        "description": "Get the current date and time",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_weather",
        "function": get_weather,
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name or location"
                },
                "units": {
                    "type": "string",
                    "description": "The units to use (metric, imperial, standard)",
                    "enum": ["metric", "imperial", "standard"],
                    "default": "metric"
                }
            },
            "required": ["location"]
        }
    }
]