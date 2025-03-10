# Claude API Integration

A Python project that demonstrates how to interact with Anthropic's Claude API.

## Features

- Environment variable management from .env files
- Structured LLM class for easy interaction with Claude
- Support for both simple prompts and conversation history

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

Basic usage example:

```python
from src.llm import LLM
from src.utils.environment import load_env_from_file

# Load environment variables
load_env_from_file('.env')

# Create LLM instance
llm = LLM()

# Generate a response
response = llm.generate(
    prompt="Why is the sky blue?",
    system="You are a helpful assistant.",
    max_tokens=1000
)

print(response)
```

## Project Structure

- `src/` - Main source code
  - `main.py` - Example script
  - `llm.py` - LLM class for interacting with Claude
  - `utils/` - Utility functions
    - `environment.py` - Environment variable handling

## Requirements

- Python 3.9+
- Anthropic API key
- Required packages in requirements.txt 