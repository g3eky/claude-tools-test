import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path to make imports work
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from src.utils.environment import load_env_from_file
# from src.utils.sample_tools import sample_tools as llm_tools
# from src.utils.magic_tools import magic_tools as llm_tools
# from src.utils.obsidian_tools import obsidian_tools as llm_tools
from src.utils.pokemon_tools import pokemon_tools as llm_tools
from src.llm import LLM

# Load environment variables from .env file
env_vars = load_env_from_file('.env')

# Create an instance of the LLM class
llm = LLM()


for tool in llm_tools:
    llm.register_tool(**tool)


def print_tool_usage(tool_usage):
    """Print tool usage information in a readable format."""
    if not tool_usage:
        print("No tools were used.")
        return
    
    print("\nTool Usage:")
    for i, usage in enumerate(tool_usage, 1):
        print(f"\n[Tool Call {i}]")
        print(f"Tool: {usage['tool']}")
        print(f"Input: {usage['input']}")
        if 'error' in usage:
            print(f"Error: {usage['error']}")
        else:
            print(f"Output: {json.dumps(usage['output'], indent=2)}")

def main():
    """Main function to demonstrate the LLM with tools."""
    print("Claude with Tools Demo")
    print("Type 'exit' to quit\n")
    
    # system_prompt = """You are a helpful assistant with access to tools that can 
    # create and update markdown files in a Obsidian vault. You can link a file in another
    # file with the [[file_name]] syntax.
    # """

    # system_prompt = """You are an assistant to me. Do what ever I say. You have spells under your arsenal.  """
    system_prompt = "You are a pokemon trainer. You have can have pokemons. You can store and retrieve pokemons."

    # system_prompt = """You are a helpful assistant that can use tools to help the user. You can give me time and weather"""
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # print("\nThinking...")
        result = llm.generate_with_tools(
            prompt=user_input,
            system=system_prompt,
            max_iterations=50,
            temperature=0.7
        )
        
        print(f"\nClaude: {result['response']}")
        
        # if 'tool_usage' in result and result['tool_usage']:
        #     print_tool_usage(result['tool_usage'])
        
        if 'warning' in result:
            print(f"\nWarning: {result['warning']}")

if __name__ == "__main__":
    main()
