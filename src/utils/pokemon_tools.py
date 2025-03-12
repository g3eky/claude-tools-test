from typing import Dict, Any, List

# Store Pokémon on the belt
pokemon_belt = {}

def list_pokemon_types() -> Dict[str, Any]:
    """
    Lists all the basic Pokémon types.
    
    Returns:
        A dictionary with the list of Pokémon types
    """
    print("[TOOL CALLED] list_pokemon_types")
    types = ["Fire", "Water", "Grass"]
    print(f"Available Pokémon types: {', '.join(types)}")
    
    return {
        "types": types,
        "count": len(types)
    }

def have_pokemon(pokemon_name: str, pokemon_type: str, trainer_name: str) -> Dict[str, Any]:
    """
    Adds a Pokémon to the trainer's collection.
    
    Args:
        pokemon_name: The name of the Pokémon
        pokemon_type: The type of the Pokémon (Fire, Water, or Grass)
        trainer_name: The name of the Pokémon's trainer
        
    Returns:
        A dictionary with information about the added Pokémon
    """
    print(f"[TOOL CALLED] have_pokemon with {pokemon_name}, {pokemon_type}, {trainer_name}")
    # Validate the Pokémon type
    valid_types = ["Fire", "Water", "Grass"]
    if pokemon_type not in valid_types:
        message = f"Invalid Pokémon type: {pokemon_type}. Valid types are: {', '.join(valid_types)}"
        print(message)
        return {
            "status": "error",
            "message": message
        }
    
    # Store the Pokémon with trainer information
    if trainer_name not in pokemon_belt:
        pokemon_belt[trainer_name] = {}
    
    pokemon_belt[trainer_name][pokemon_name] = pokemon_type
    message = f"{trainer_name} now has {pokemon_name} ({pokemon_type})!"
    print(message)
    
    return {
        "pokemon": pokemon_name,
        "type": pokemon_type,
        "trainer": trainer_name,
        "status": "added",
        "message": message,
        "trainer_pokemon_count": len(pokemon_belt[trainer_name])
    }

def get_advantageous_type(pokemon_type: str) -> Dict[str, Any]:
    """
    Returns the type that has an advantage against the given type.
    
    Args:
        pokemon_type: The type to find an advantage against (Fire, Water, or Grass)
        
    Returns:
        A dictionary with information about the advantageous type
    """
    print(f"[TOOL CALLED] get_advantageous_type with {pokemon_type}")
    # Define type advantages
    type_advantages = {
        "Fire": "Water",
        "Water": "Grass",
        "Grass": "Fire"
    }
    
    # Validate the Pokémon type
    valid_types = ["Fire", "Water", "Grass"]
    if pokemon_type not in valid_types:
        message = f"Invalid Pokémon type: {pokemon_type}. Valid types are: {', '.join(valid_types)}"
        print(message)
        return {
            "status": "error",
            "message": message
        }
    
    # Get the advantageous type
    advantageous_type = type_advantages[pokemon_type]
    message = f"{advantageous_type} type has an advantage against {pokemon_type} type!"
    print(message)
    
    return {
        "original_type": pokemon_type,
        "advantageous_type": advantageous_type,
        "message": message
    }

def list_trainer_pokemon(trainer_name: str) -> Dict[str, Any]:
    """
    Lists all Pokémon that a given trainer has.
    
    Args:
        trainer_name: The name of the trainer whose Pokémon to list
        
    Returns:
        A dictionary with information about the trainer's Pokémon
    """
    print(f"[TOOL CALLED] list_trainer_pokemon with {trainer_name}")
    
    # Check if trainer exists
    if trainer_name not in pokemon_belt:
        message = f"Trainer {trainer_name} has no Pokémon yet!"
        print(message)
        return {
            "trainer": trainer_name,
            "pokemon": {},
            "count": 0,
            "message": message
        }
    
    # Get trainer's Pokémon
    trainer_pokemon = pokemon_belt[trainer_name]
    pokemon_list = [f"{name} ({type_})" for name, type_ in trainer_pokemon.items()]
    
    message = f"{trainer_name}'s Pokémon: {', '.join(pokemon_list)}" if pokemon_list else f"{trainer_name} has no Pokémon yet!"
    print(message)
    
    return {
        "trainer": trainer_name,
        "pokemon": trainer_pokemon,
        "count": len(trainer_pokemon),
        "pokemon_list": pokemon_list,
        "message": message
    }

# Define the tools for LLM integration
pokemon_tools = [
    {
        "name": "list_pokemon_types",
        "function": list_pokemon_types,
        "description": "List all available Pokémon types",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "have_pokemon",
        "function": have_pokemon,
        "description": "Add a Pokémon to a trainer's collection",
        "input_schema": {
            "type": "object",
            "properties": {
                "pokemon_name": {
                    "type": "string",
                    "description": "The name of the Pokémon to add"
                },
                "pokemon_type": {
                    "type": "string",
                    "description": "The type of the Pokémon (Fire, Water, or Grass)"
                },
                "trainer_name": {
                    "type": "string",
                    "description": "The name of the Pokémon's trainer"
                }
            },
            "required": ["pokemon_name", "pokemon_type", "trainer_name"]
        }
    },
    {
        "name": "get_advantageous_type",
        "function": get_advantageous_type,
        "description": "Get the type that has an advantage against a given type",
        "input_schema": {
            "type": "object",
            "properties": {
                "pokemon_type": {
                    "type": "string",
                    "description": "The Pokémon type to find an advantage against (Fire, Water, or Grass)"
                }
            },
            "required": ["pokemon_type"]
        }
    },
    {
        "name": "list_trainer_pokemon",
        "function": list_trainer_pokemon,
        "description": "List all Pokémon that a given trainer has",
        "input_schema": {
            "type": "object",
            "properties": {
                "trainer_name": {
                    "type": "string",
                    "description": "The name of the trainer whose Pokémon to list"
                }
            },
            "required": ["trainer_name"]
        }
    }
] 