import anthropic
import os
from typing import List, Dict, Any, Optional, Union

class LLM:
    """
    A class to handle interactions with Language Models (specifically Anthropic's Claude).
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-7-sonnet-20250219"):
        """
        Initialize the LLM with API key and default model.
        
        Args:
            api_key: The API key for Anthropic. If None, will use ANTHROPIC_API_KEY from environment.
            model: The model to use for generation. Defaults to claude-3-7-sonnet.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either directly or via ANTHROPIC_API_KEY environment variable")
        
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def generate(self, 
                prompt: str, 
                system: Optional[str] = None,
                max_tokens: int = 1000,
                temperature: float = 1.0) -> str:
        """
        Generate a response from the language model.
        
        Args:
            prompt: The user prompt to send to the model
            system: Optional system prompt to control model behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness (0-1)
            
        Returns:
            The generated text response
        """
        message_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        if system:
            message_params["system"] = system
            
        response = self.client.messages.create(**message_params)
        
        # Extract the text content from the response
        if response.content:
            return response.content[0].text
        return ""
    
    def generate_with_history(self,
                             messages: List[Dict[str, Any]],
                             system: Optional[str] = None,
                             max_tokens: int = 1000,
                             temperature: float = 1.0) -> str:
        """
        Generate a response with a conversation history.
        
        Args:
            messages: List of message objects with role and content
            system: Optional system prompt to control model behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness (0-1)
            
        Returns:
            The generated text response
        """
        message_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }
        
        if system:
            message_params["system"] = system
            
        response = self.client.messages.create(**message_params)
        
        # Extract the text content from the response
        if response.content:
            return response.content[0].text
        return "" 