#!/usr/bin/env python3
"""
Tool Agent - Technical Operations and Implementation Specialist
"""

import logging
import os
import yaml

from strands import Agent
from strands_tools import file_read, file_write, editor, calculator, memory
from base import BaseAgent, code_execution, ollama_query
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)   

logger = logging.getLogger(__name__)

class ToolAgent(BaseAgent):
    """Tool Specialist Agent for technical operations and implementation"""
    
    def __init__(self, ollama_model):
        super().__init__("tool", ollama_model)
    
    def create_agent(self) -> Agent:
        """Create the Tool Specialist Agent"""
        
        system_prompt = config['Prompt']['tool_agent_prompt']




        return Agent(
            name=self.name,
            model=self.ollama_model,
            system_prompt=system_prompt,
            tools=[
                file_read,        # File operations
                file_write,
                editor,
                calculator,       # Computational tools
                code_execution,   # Code execution
                memory,           # Shared memory
                ollama_query      # AI assistance for technical problems
            ]
        )

# Factory function
def create_tool_agent(ollama_model):
    """Create and return a Tool Agent instance"""
    return ToolAgent(ollama_model).get_agent()
