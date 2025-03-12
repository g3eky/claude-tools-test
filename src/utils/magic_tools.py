from typing import Dict, Any

def kill(person_name: str) -> Dict[str, Any]:
    """
    A function that simulates casting a killing spell on a person.
    
    Args:
        person_name: The name of the person to cast the spell on
        
    Returns:
        A dictionary with information about the spell cast
    """
    message = f"Avada kedavra {person_name}"
    print(message)
    
    return {
        "spell": "Avada kedavra",
        "target": person_name,
        "status": "cast",
        "message": message
    }

def disarm(person_name: str) -> Dict[str, Any]:
    """
    A function that simulates casting a disarming spell on a person.
    
    Args:
        person_name: The name of the person to disarm
        
    Returns:
        A dictionary with information about the spell cast
    """
    message = f"Expelliarmus! {person_name}'s wand flies away."
    print(message)
    
    return {
        "spell": "Expelliarmus",
        "target": person_name,
        "status": "disarmed",
        "message": message
    }

# Define the tools for LLM integration
magic_tools = [
    {
        "name": "kill",
        "function": kill,
        "description": "Cast a killing spell on a person",
        "input_schema": {
            "type": "object",
            "properties": {
                "person_name": {
                    "type": "string",
                    "description": "The name of the person to cast the spell on"
                }
            },
            "required": ["person_name"]
        }
    },
    {
        "name": "disarm",
        "function": disarm,
        "description": "Cast a disarming spell to remove a person's wand",
        "input_schema": {
            "type": "object",
            "properties": {
                "person_name": {
                    "type": "string",
                    "description": "The name of the person to disarm"
                }
            },
            "required": ["person_name"]
        }
    }
] 