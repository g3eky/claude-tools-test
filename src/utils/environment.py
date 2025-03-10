import os

def load_env_from_file(env_file_path):
    """
    Load environment variables from a file.
    
    The file should contain key=value pairs, one per line.
    Values can optionally be surrounded by double quotes, which will be removed.
    
    Args:
        env_file_path (str): Path to the environment file
        
    Returns:
        dict: Dictionary of loaded environment variables
    """
    env_vars = {}
    
    try:
        with open(env_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Split by the first equals sign
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove surrounding quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    
                    # Set environment variable
                    os.environ[key] = value
                    env_vars[key] = value
        
        return env_vars
    except FileNotFoundError:
        print(f"Warning: Environment file {env_file_path} not found.")
        return {}
    except Exception as e:
        print(f"Error loading environment file: {e}")
        return {} 