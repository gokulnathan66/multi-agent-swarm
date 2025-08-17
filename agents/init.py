#!/usr/bin/env python3
"""
Multi-Agent Swarm Base Classes and Utilities
"""

import json
import requests
import logging
import yaml
import os
from typing import Dict, Any, Optional, List
from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands.multiagent import Swarm
from strands_tools import file_read, file_write, editor, memory, calculator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

# Enable debug logs for multi-agent operations
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)

class OllamaClient:
    """Enhanced client for communicating with Ollama local model"""
    
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

# Global Ollama client instance
ollama_client = None

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

@tool
def web_search(query: str) -> str:
    """Simulate web search functionality"""
    return f"Search results for '{query}': [Simulated search results would appear here]"

@tool  
def code_execution(code: str, language: str = "python") -> str:
    """Execute code safely in a sandboxed environment"""
    return f"Code execution result: [Simulated execution of {language} code]"

class SwarmConfig:
    """Configuration management for the swarm"""
    
    def __init__(self, config_path: str = "config.yml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                return self.create_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        default_config = {
            "ollama": {
                "host": "http://localhost:11434",
                "default_model": "llama3.2:1b",
                "temperature": 0.7,
                "keep_alive": "10m"
            },
            "swarm": {
                "max_handoffs": 25,
                "max_iterations": 30,
                "execution_timeout": 1200.0,  # 20 minutes
                "node_timeout": 300.0,        # 5 minutes per agent
                "repetitive_handoff_detection_window": 8,
                "repetitive_handoff_min_unique_agents": 3
            }
        }
        
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Error saving default config: {e}")
        
        return default_config

class BaseAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, ollama_model: OllamaModel):
        self.name = name
        self.ollama_model = ollama_model
        self.agent = None
    
    def create_agent(self) -> Agent:
        """Create the Strands agent - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement create_agent method")
    
    def get_agent(self) -> Agent:
        """Get the created agent instance"""
        if self.agent is None:
            self.agent = self.create_agent()
        return self.agent
