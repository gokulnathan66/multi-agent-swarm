#!/usr/bin/env python3
"""
Search Agent - Web Search and Information Retrieval Specialist
"""

import logging
import os
import yaml

from strands import Agent
from strands_tools import memory
from base import BaseAgent, web_search, ollama_query
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)   

logger = logging.getLogger(__name__)

class SearchAgent(BaseAgent):
    """Search Specialist Agent for web search and information retrieval"""
    
    def __init__(self, ollama_model):
        super().__init__("search", ollama_model)
    
    def create_agent(self) -> Agent:
        """Create the Search Specialist Agent"""
        
        system_prompt = config['Prompt']['search_agent_prompt']



        return Agent(
            name=self.name,
            model=self.ollama_model,
            system_prompt=system_prompt,
            tools=[
                web_search,       # Primary search capability
                memory,           # Shared memory access
                ollama_query      # AI assistance for search optimization
            ]
        )

# Factory function
def create_search_agent(ollama_model):
    """Create and return a Search Agent instance"""
    return SearchAgent(ollama_model).get_agent()
