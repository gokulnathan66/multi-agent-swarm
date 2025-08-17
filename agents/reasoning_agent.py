#!/usr/bin/env python3
"""
Reasoning Agent - Logic and Analysis Specialist
"""

import logging
from strands import Agent
from strands_tools import memory, calculator
from . import BaseAgent, ollama_query
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)   

logger = logging.getLogger(__name__)

class ReasoningAgent(BaseAgent):
    """Reasoning Specialist Agent for logic and analysis"""
    
    def __init__(self, ollama_model):
        super().__init__("reasoning", ollama_model)
    
    def create_agent(self) -> Agent:
        """Create the Reasoning Specialist Agent"""
        
        system_prompt = config['Prompt']['reasoning_agent_prompt']

        return Agent(
            name=self.name,
            model=self.ollama_model,
            system_prompt=system_prompt,
            tools=[
                memory,           # Shared memory for reasoning chains
                calculator,       # Computational support
                ollama_query      # AI assistance for complex reasoning
            ]
        )

# Factory function
def create_reasoning_agent(ollama_model):
    """Create and return a Reasoning Agent instance"""
    return ReasoningAgent(ollama_model).get_agent()






































