import os
import sys
from pathlib import Path

# Add the project root to the Python path to make imports work
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from utils.environment import load_env_from_file
from llm import LLM

# Load environment variables from .env file
env_vars = load_env_from_file('.env')

# Create an instance of the LLM class
llm = LLM()

# Generate a poetic response
response = llm.generate(
    prompt="Why is the ocean salty?",
    system="You are a world-class poet. Respond only with short poems.",
    max_tokens=1000,
    temperature=1
)

print(response)
