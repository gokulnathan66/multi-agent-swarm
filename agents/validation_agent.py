#!/usr/bin/env python3
"""
Validation Agent - Quality Assurance and Verification Specialist
"""

import logging
from strands import Agent
from strands_tools import memory, file_read
from . import BaseAgent, ollama_query

import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)   

logger = logging.getLogger(__name__)

class ValidationAgent(BaseAgent):
    """Validation Specialist Agent for quality assurance and verification"""
    
    def __init__(self, ollama_model):
        super().__init__("validation", ollama_model)
    
    def create_agent(self) -> Agent:
        """Create the Validation Specialist Agent"""
        
        system_prompt = config['Prompt']['validation_agent_prompt']


        return Agent(
            name=self.name,
            model=self.ollama_model,
            system_prompt=system_prompt,
            tools=[
                memory,           # Access to shared work for validation
                file_read,        # Review files and documents
                ollama_query      # AI assistance for validation criteria
            ]
        )

# Factory function
def create_validation_agent(ollama_model):
    """Create and return a Validation Agent instance"""
    return ValidationAgent(ollama_model).get_agent()
