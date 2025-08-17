#!/usr/bin/env python3
"""
Strands Agent with Ollama Local Model Integration

This script creates a Strands agent that communicates with a local Ollama model
and includes various tools for enhanced functionality.
"""

import json
import requests
import logging
from typing import Dict, Any, Optional
from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import file_read, file_write, editor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for communicating with Ollama local model"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:1b"):
        self.base_url = base_url
        self.model = model
        self.headers = {"Content-Type": "application/json"}
    
    def generate(self, prompt: str, stream: bool = False) -> Dict[str, Any]:
        """Generate response from Ollama model"""
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with Ollama: {e}")
            return {"error": str(e)}
    
    def chat(self, messages: list, stream: bool = False) -> Dict[str, Any]:
        """Chat with Ollama model using message history"""
        url = f"{self.base_url}/api/chat"
        data = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with Ollama: {e}")
            return {"error": str(e)}
    
    def list_models(self) -> Dict[str, Any]:
        """List available Ollama models"""
        url = f"{self.base_url}/api/tags"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing models: {e}")
            return {"error": str(e)}

@tool
def ollama_query(prompt: str, use_chat: bool = False) -> str:
    """
    Query the Ollama model with a prompt
    
    Args:
        prompt: The prompt to send to the model
        use_chat: Whether to use chat format or generate format
    
    Returns:
        str: The model's response
    """
    # Use the global Ollama client
    if use_chat:
        messages = [{"role": "user", "content": prompt}]
        result = ollama_client.chat(messages)
        if "error" in result:
            return f"Error: {result['error']}"
        return result.get("message", {}).get("content", "No response received")
    else:
        result = ollama_client.generate(prompt)
        if "error" in result:
            return f"Error: {result['error']}"
        return result.get("response", "No response received")

def main():
    """Main function to create and run the Strands agent"""
    
    global ollama_client
    
    # Initialize Ollama client
    ollama_client = OllamaClient(model="llama3.2:1b")
    
    # Test Ollama connection
    logger.info("Testing Ollama connection...")
    models = ollama_client.list_models()
    if "error" in models:
        logger.error(f"Cannot connect to Ollama: {models['error']}")
        logger.error("Make sure Ollama is running on localhost:11434")
        return
    
    logger.info(f"Available models: {[model['name'] for model in models.get('models', [])]}")
    
    # Create Ollama model instance for Strands
    ollama_model = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.2:1b",
        temperature=0.7,
        keep_alive="10m"
    )
    
    # Define system prompt for the agent
    SYSTEM_PROMPT = """You are an intelligent AI assistant powered by a local Ollama model.
    You have access to various tools including:
    
    1. File operations (read, write, edit files)
    2. Local Ollama model queries for AI assistance
    3. General computational and analytical capabilities
    
    Key capabilities:
    - Answer questions using the local Ollama model
    - Perform file operations
    - Help with coding and technical tasks
    - Provide analysis and insights
    
    Always be helpful, accurate, and provide clear explanations.
    When using the Ollama model, mention that responses come from your local AI model.
    """
    
    # Create Strands agent with tools
    agent = Agent(
        model=ollama_model,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            file_read,      # File reading tool
            file_write,     # File writing tool
            editor,         # File editing tool
            ollama_query    # Custom Ollama query tool
        ]
    )
    
    logger.info("Strands agent initialized successfully!")
    logger.info("Available tools: file_read, file_write, editor, ollama_query")
    
    # Interactive chat loop
    print("\n=== Strands Agent with Ollama Integration ===")
    print("Type 'quit' to exit, 'help' for commands")
    print("Examples:")
    print("- 'Query Ollama: What is Python?'")
    print("- 'Create a file called test.txt with content Hello World'")
    print("- 'Read the file config.json'")
    print("- 'Ask Ollama to explain quantum computing'")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("- Direct conversation with the agent")
                print("- File operations: 'read file.txt', 'write to file.txt', etc.")
                print("- Ollama queries: 'ask ollama about...', 'query: ...'")
                print("- 'models' - list available Ollama models")
                print("- 'quit' - exit the program")
                continue
            
            if user_input.lower() == 'models':
                models = ollama_client.list_models()
                if "error" not in models:
                    print("\nAvailable Ollama models:")
                    for model in models.get('models', []):
                        print(f"- {model['name']}")
                else:
                    print(f"Error listing models: {models['error']}")
                continue
            
            if not user_input:
                continue
            
            # Get response from Strands agent
            print("\nAgent: Processing your request...")
            response = agent(user_input)
            print(f"Agent: {response}")
            
            # Add to conversation history
            conversation_history.append({
                "user": user_input,
                "agent": response
            })
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error in conversation loop: {e}")
            print(f"Error: {e}")

def test_agent():
    """Test function to verify agent functionality"""
    
    print("=== Testing Strands Agent with Ollama ===")
    
    global ollama_client
    
    # Initialize components
    ollama_client = OllamaClient(model="llama3.2:1b")
    
    # Test Ollama connection
    test_prompt = "What is artificial intelligence?"
    result = ollama_query(test_prompt)
    print(f"Ollama test result: {result[:100]}...")
    
    # Create Ollama model for Strands
    ollama_model = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.2:1b"
    )
    
    # Create agent
    agent = Agent(
        model=ollama_model,
        system_prompt="You are a helpful AI assistant with access to local AI models and file operations.",
        tools=[file_read, file_write, editor, ollama_query]
    )
    
    # Test queries
    test_queries = [
        "Hello, can you introduce yourself?",
        "Create a file called test_output.txt with the content 'Hello from Strands Agent'",
        "Ask the local AI model: What are the benefits of local AI models?"
    ]
    
    for query in test_queries:
        print(f"\nTest Query: {query}")
        try:
            response = agent(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_agent()
    else:
        main()
