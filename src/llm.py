import anthropic
import os
import json
from typing import List, Dict, Any, Optional, Union, Callable

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
        self.tools = {}
    
    def register_tool(self, name: str, function: Callable, description: str):
        """
        Register a tool that the LLM can use.
        
        Args:
            name: The name of the tool
            function: The function to call when the tool is used
            description: A description of what the tool does
        """
        self.tools[name] = {
            "function": function,
            "description": description
        }
    
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
    
    def generate_with_tools(self,
                           prompt: str,
                           system: Optional[str] = None,
                           max_tokens: int = 1000,
                           temperature: float = 0.7,
                           max_iterations: int = 5) -> Dict[str, Any]:
        """
        Generate a response with tool use capability.
        
        Args:
            prompt: The user prompt to send to the model
            system: Optional system prompt to control model behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness (0-1)
            max_iterations: Maximum number of tool use iterations
            
        Returns:
            Dictionary containing the final response and tool usage history
        """
        if not self.tools:
            # If no tools are registered, fall back to regular generation
            return {
                "response": self.generate(prompt, system, max_tokens, temperature),
                "tool_usage": []
            }
        
        # Prepare tools in the format expected by Claude
        tools = []
        for name, tool_info in self.tools.items():
            tools.append({
                "name": name,
                "description": tool_info["description"]
            })
        
        # Initial message from the user
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        tool_usage = []
        iterations = 0
        
        while iterations < max_iterations:
            iterations += 1
            
            # Create message parameters
            message_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages,
                "tools": tools
            }
            
            if system:
                message_params["system"] = system
            
            # Get response from Claude
            response = self.client.messages.create(**message_params)
            
            # Check if the response contains tool calls
            tool_calls = []
            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_calls.append({
                        "name": content_block.name,
                        "input": content_block.input
                    })
            
            if not tool_calls:
                # No tool calls, return the final response
                final_response = ""
                for content_block in response.content:
                    if content_block.type == "text":
                        final_response += content_block.text
                
                return {
                    "response": final_response,
                    "tool_usage": tool_usage
                }
            
            # Process tool calls
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_input = tool_call["input"]
                
                if tool_name in self.tools:
                    try:
                        # Execute the tool
                        tool_function = self.tools[tool_name]["function"]
                        tool_result = tool_function(**json.loads(tool_input))
                        
                        # Record tool usage
                        tool_usage.append({
                            "tool": tool_name,
                            "input": tool_input,
                            "output": tool_result
                        })
                        
                        # Add tool response to messages
                        messages.append({
                            "role": "assistant",
                            "content": [
                                {
                                    "type": "tool_use",
                                    "name": tool_name,
                                    "input": tool_input
                                }
                            ]
                        })
                        
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": len(tool_usage),  # Simple ID based on usage count
                                    "content": str(tool_result)
                                }
                            ]
                        })
                    except Exception as e:
                        # Handle tool execution errors
                        error_message = f"Error executing tool {tool_name}: {str(e)}"
                        messages.append({
                            "role": "system",
                            "content": error_message
                        })
                        tool_usage.append({
                            "tool": tool_name,
                            "input": tool_input,
                            "error": error_message
                        })
                else:
                    # Tool not found
                    error_message = f"Tool {tool_name} not found"
                    messages.append({
                        "role": "system",
                        "content": error_message
                    })
                    tool_usage.append({
                        "tool": tool_name,
                        "input": tool_input,
                        "error": error_message
                    })
        
        # If we've reached the maximum number of iterations, return the last response
        final_response = ""
        for content_block in response.content:
            if content_block.type == "text":
                final_response += content_block.text
        
        return {
            "response": final_response,
            "tool_usage": tool_usage,
            "warning": "Maximum number of tool use iterations reached"
        } 