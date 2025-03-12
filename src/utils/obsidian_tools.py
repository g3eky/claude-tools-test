import os
import datetime
from typing import Dict, Any, Optional

# Predefined folder for Obsidian notes
OBSIDIAN_VAULT_PATH = "/Users/neo/Desktop/test/"  # This can be changed to your actual Obsidian vault path

def ensure_vault_exists():
    """
    Ensure that the Obsidian vault directory exists.
    Creates it if it doesn't exist.
    """
    if not os.path.exists(OBSIDIAN_VAULT_PATH):
        os.makedirs(OBSIDIAN_VAULT_PATH)
        print(f"Created Obsidian vault directory at {OBSIDIAN_VAULT_PATH}")

def create_markdown_file(filename: str, content: str) -> Dict[str, Any]:
    """
    Create a new markdown file in the Obsidian vault.
    
    Args:
        filename: The name of the file to create (without path)
        content: The markdown content to write to the file
        
    Returns:
        A dictionary with information about the created file
    """
    ensure_vault_exists()
    
    # Add .md extension if not present
    if not filename.endswith('.md'):
        filename = f"{filename}.md"
    
    file_path = os.path.join(OBSIDIAN_VAULT_PATH, filename)
    
    # Check if file already exists
    file_exists = os.path.exists(file_path)
    
    # Write content to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return {
        "filename": filename,
        "path": file_path,
        "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "updated" if file_exists else "created",
        "size": len(content)
    }

def read_markdown_file(filepath: str) -> Dict[str, Any]:
    """
    Read the contents of a markdown file from the Obsidian vault.
    
    Args:
        filepath: The path to the file (relative to the vault or absolute)
        
    Returns:
        A dictionary with the file content and metadata
    """
    ensure_vault_exists()
    
    # If only filename is provided, assume it's in the vault
    if not os.path.dirname(filepath):
        # Add .md extension if not present
        if not filepath.endswith('.md'):
            filepath = f"{filepath}.md"
        file_path = os.path.join(OBSIDIAN_VAULT_PATH, filepath)
    else:
        file_path = filepath
    
    # Check if file exists
    if not os.path.exists(file_path):
        return {
            "error": "File not found",
            "filepath": file_path,
            "content": None,
            "exists": False
        }
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        "filepath": file_path,
        "content": content,
        "exists": True,
        "size": len(content),
        "last_modified": datetime.datetime.fromtimestamp(
            os.path.getmtime(file_path)
        ).strftime("%Y-%m-%d %H:%M:%S")
    }

def update_markdown_file(filename: str, content: str) -> Dict[str, Any]:
    """
    Update the contents of an existing markdown file in the Obsidian vault.
    If the file doesn't exist, it will be created.
    
    Args:
        filename: The name of the file to update (without path)
        content: The new markdown content
        
    Returns:
        A dictionary with information about the updated file
    """
    ensure_vault_exists()
    
    # Add .md extension if not present
    if not filename.endswith('.md'):
        filename = f"{filename}.md"
    
    file_path = os.path.join(OBSIDIAN_VAULT_PATH, filename)
    
    # Check if file exists
    file_exists = os.path.exists(file_path)
    
    # Get old content if file exists
    old_content = None
    if file_exists:
        with open(file_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
    
    # Write new content to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return {
        "filename": filename,
        "path": file_path,
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "updated" if file_exists else "created",
        "size": len(content),
        "size_diff": len(content) - len(old_content) if old_content is not None else len(content)
    }

# Define the tools for LLM integration
obsidian_tools = [
    {
        "name": "create_markdown_file",
        "function": create_markdown_file,
        "description": "Create a new markdown file in the Obsidian vault",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to create (without path)"
                },
                "content": {
                    "type": "string",
                    "description": "The markdown content to write to the file"
                }
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "read_markdown_file",
        "function": read_markdown_file,
        "description": "Read the contents of a markdown file from the Obsidian vault",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The path to the file (relative to the vault or absolute)"
                }
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "update_markdown_file",
        "function": update_markdown_file,
        "description": "Update the contents of an existing markdown file in the Obsidian vault",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to update (without path)"
                },
                "content": {
                    "type": "string",
                    "description": "The new markdown content"
                }
            },
            "required": ["filename", "content"]
        }
    }
] 