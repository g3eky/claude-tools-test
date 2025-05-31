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

patients = dict()

def create_patient(name: str) -> None:
    patients[name] = {}


def add_patient_gender(name: str, gender: str) -> None:
    patients[name]["gender"] = gender

def add_patient_age(name: str, age: int) -> None:
    patients[name]["age"] = age


def is_eligible_for_study(name: str) -> bool:
    return patients[name]["age"] < 18


def send_message_to_patient(name: str, message: str) -> None:
    print(f"Sending message to {name}: {message}")


def pradeep_test(name: str) -> None:
    words = str.split(name, " ")



sample_tools = [
    {
        "name": "create_patient",
        "function": create_patient,
        "description": "Create a new patient record",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The patient's name"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "add_patient_gender",
        "function": add_patient_gender,
        "description": "Add gender information to a patient record",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The patient's name"
                },
                "gender": {
                    "type": "string",
                    "description": "The patient's gender"
                }
            },
            "required": ["name", "gender"]
        }
    },
    {
        "name": "add_patient_age",
        "function": add_patient_age,
        "description": "Add age information to a patient record",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The patient's name"
                },
                "age": {
                    "type": "integer",
                    "description": "The patient's age"
                }
            },
            "required": ["name", "age"]
        }
    },
    {
        "name": "is_eligible_for_study",
        "function": is_eligible_for_study,
        "description": "Check if a patient is eligible for a study",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The patient's name"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "send_message_to_patient",
        "function": send_message_to_patient,
        "description": "Send a message to a patient",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The patient's name"
                },
                "message": {
                    "type": "string",
                    "description": "The message to send"
                }
            },
            "required": ["name", "message"]
        }
    }
] 