#!/usr/bin/env python3
# aka the master agent
"""
Hynicl Agent - Master Coordinator and Specialized Agent

This agent serves as both the master coordinator for the swarm and provides
specialized domain expertise.
"""

import logging
from strands import Agent
from strands_tools import memory, file_read, file_write, editor, calculator
from . import BaseAgent, ollama_query
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)   

logger = logging.getLogger(__name__)

class HyniclAgent(BaseAgent):
    """
    Hynicl Agent - Master Coordinator with specialized capabilities
    
    This agent combines master coordination responsibilities with domain-specific expertise.
    It orchestrates the swarm while providing specialized analytical capabilities.
    """
    
    def __init__(self, ollama_model):
        super().__init__("hynicl", ollama_model)
        self.coordination_mode = True
        self.specialist_mode = True
    
    def create_agent(self) -> Agent:
        """Create the Hynicl Agent with master coordination capabilities"""

        system_prompt = config['Prompt']['hynicl_agent_prompt']

        return Agent(
            name=self.name,
            model=self.ollama_model,
            system_prompt=system_prompt,
            tools=[
                memory,           # Shared memory access
                ollama_query,     # Direct Ollama access
                file_read,        # File operations
                file_write,
                editor,
                calculator        # Computational tools
            ]
        )
    
    def get_coordination_strategy(self, task: str) -> str:
        """Analyze task and determine coordination strategy"""
        
        # Simple heuristics for coordination decisions
        coordination_keywords = [
            "research and", "analyze and create", "find and validate", 
            "calculate and explain", "search and summarize",
            "create and test", "design and implement"
        ]
        
        specialist_keywords = [
            "coordinate", "orchestrate", "manage", "oversee",
            "synthesize", "integrate", "combine", "merge"
        ]
        
        task_lower = task.lower()
        
        needs_coordination = any(keyword in task_lower for keyword in coordination_keywords)
        is_specialist_task = any(keyword in task_lower for keyword in specialist_keywords)
        
        if needs_coordination:
            return "multi_agent_coordination"
        elif is_specialist_task:
            return "specialist_direct"
        else:
            return "assess_complexity"
    
    def execute_as_master(self, task: str) -> str:
        """Execute task in master coordination mode"""
        strategy = self.get_coordination_strategy(task)
        
        logger.info(f"Hynicl Master executing with strategy: {strategy}")
        
        if strategy == "multi_agent_coordination":
            return f"[COORDINATION MODE] Analyzing task for multi-agent delegation: {task}"
        elif strategy == "specialist_direct":
            return f"[SPECIALIST MODE] Handling specialized task directly: {task}"
        else:
            return f"[ASSESSMENT MODE] Evaluating task complexity: {task}"

# Factory function for easy import
def create_hynicl_agent(ollama_model):
    """Create and return a Hynicl Agent instance"""
    return HyniclAgent(ollama_model).get_agent()
