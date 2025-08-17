#!/usr/bin/env python3
"""
Multi-Agent Swarm Main Orchestrator

This is the main entry point for the multi-agent swarm system.
"""

import logging
import sys
import os
from typing import Dict, Any

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from agents import SwarmConfig, OllamaClient, ollama_client as global_ollama_client
from agents.hynicl_agent import create_hynicl_agent
from agents.search_agent import create_search_agent
from agents.reasoning_agent import create_reasoning_agent
from agents.tool_agent import create_tool_agent
from agents.validation_agent import create_validation_agent

from strands.models.ollama import OllamaModel
from strands.multiagent import Swarm

logger = logging.getLogger(__name__)

class MultiAgentSwarm:
    """Main orchestrator for the multi-agent swarm"""
    
    def __init__(self):
        self.config = SwarmConfig()
        self.ollama_client = None
        self.ollama_model = None
        self.agents = {}
        self.swarm = None
        
        self.initialize_ollama()
        self.create_specialized_agents()
        self.create_swarm()
    
    def initialize_ollama(self):
        """Initialize Ollama client and model"""
        global global_ollama_client
        
        ollama_config = self.config.config["ollama"]
        
        # Initialize Ollama client
        self.ollama_client = OllamaClient(
            base_url=ollama_config["host"],
            model=ollama_config["default_model"]
        )
        
        # Set global client for tools
        global_ollama_client = self.ollama_client
        
        # Test connection
        logger.info("Testing Ollama connection...")
        models = self.ollama_client.list_models()
        if "error" in models:
            logger.error(f"Cannot connect to Ollama: {models['error']}")
            raise ConnectionError("Make sure Ollama is running on localhost:11434")
        
        logger.info(f"Available models: {[model['name'] for model in models.get('models', [])]}")
        
        # Create Ollama model instance
        self.ollama_model = OllamaModel(
            host=ollama_config["host"],
            model_id=ollama_config["default_model"],
            temperature=ollama_config["temperature"],
            keep_alive=ollama_config["keep_alive"]
        )
    
    def create_specialized_agents(self):
        """Create all specialized agents for the swarm"""
        
        logger.info("Creating specialized agents...")
        
        # Create each agent using their factory functions
        self.agents["hynicl"] = create_hynicl_agent(self.ollama_model)
        self.agents["search"] = create_search_agent(self.ollama_model)
        self.agents["reasoning"] = create_reasoning_agent(self.ollama_model)
        self.agents["tool"] = create_tool_agent(self.ollama_model)
        self.agents["validation"] = create_validation_agent(self.ollama_model)
        
        logger.info(f"Created {len(self.agents)} specialized agents")
        logger.info(f"Agents: {list(self.agents.keys())}")
    
    def create_swarm(self):
        """Create the swarm with all agents"""
        swarm_config = self.config.config["swarm"]
        
        # Convert agents dict to list for swarm
        agent_list = list(self.agents.values())
        
        self.swarm = Swarm(
            agent_list,
            max_handoffs=swarm_config["max_handoffs"],
            max_iterations=swarm_config["max_iterations"],
            execution_timeout=swarm_config["execution_timeout"],
            node_timeout=swarm_config["node_timeout"],
            repetitive_handoff_detection_window=swarm_config["repetitive_handoff_detection_window"],
            repetitive_handoff_min_unique_agents=swarm_config["repetitive_handoff_min_unique_agents"]
        )
        
        logger.info("Multi-agent swarm created successfully!")
    
    def execute_task(self, task: str) -> Any:
        """Execute a task using the swarm"""
        logger.info(f"🚀 Executing task: {task}")
        
        try:
            result = self.swarm(task)
            
            logger.info("✅ Task execution completed")
            logger.info(f"📊 Status: {result.status}")
            logger.info(f"🔄 Agent sequence: {[node.node_id for node in result.node_history]}")
            
            return result
        except Exception as e:
            logger.error(f"❌ Error executing task: {e}")
            raise
    
    def run_interactive_mode(self):
        """Run the swarm in interactive mode"""
        print("\n" + "="*70)
        print("🤖 HYNICL MULTI-AGENT SWARM WITH OLLAMA 🤖")
        print("="*70)
        print(f"🎯 Master Coordinator: HYNICL")
        print(f"🔧 Specialists: {', '.join([k for k in self.agents.keys() if k != 'hynicl'])}")
        print(f"🏠 Local AI: {self.config.config['ollama']['default_model']}")
        print("="*70)
        print("💡 Type 'help' for commands, 'quit' to exit")
        print("The Hynicl master will coordinate specialists to solve your tasks!")
        print("="*70)
        
        while True:
            try:
                user_input = input("\n🎯 Task: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Swarm shutting down. Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'agents':
                    self.show_agents()
                    continue
                
                if user_input.lower() == 'config':
                    self.show_config()
                    continue
                
                if not user_input:
                    continue
                
                print(f"\n🚀 Hynicl Swarm processing: {user_input}")
                print("-" * 60)
                
                result = self.execute_task(user_input)
                
                print(f"\n✅ Task completed by Hynicl Swarm!")
                print(f"📊 Agent flow: {' → '.join([node.node_id for node in result.node_history])}")
                print(f"🎯 Result:\n{result}")
                
            except KeyboardInterrupt:
                print("\n👋 Swarm interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show help information"""
        print("\n📚 HYNICL SWARM COMMANDS:")
        print("• Direct task description - Hynicl will coordinate agents automatically")
        print("• 'agents' - Show available agents and roles")
        print("• 'config' - Show current swarm configuration")  
        print("• 'help' - Show this help message")
        print("• 'quit' - Exit the swarm")
        print("\n💡 EXAMPLE TASKS:")
        print("• 'Research quantum computing and create a technical report'")
        print("• 'Search for Python best practices and validate the information'")
        print("• 'Analyze this dataset and implement visualization code'")
        print("• 'Find information about AI ethics and reason through the implications'")
    
    def show_agents(self):
        """Show available agents and their roles"""
        print("\n🤖 HYNICL SWARM AGENTS:")
        print("• HYNICL (Master): Coordinates swarm + domain expertise")
        print("• SEARCH: Web search and information retrieval")
        print("• REASONING: Logic analysis and decision making")  
        print("• TOOL: Technical implementation and file operations")
        print("• VALIDATION: Quality assurance and verification")
    
    def show_config(self):
        """Show current configuration"""
        print("\n⚙️ CURRENT CONFIGURATION:")
        print(f"• Ollama Host: {self.config.config['ollama']['host']}")
        print(f"• Model: {self.config.config['ollama']['default_model']}")
        print(f"• Max Handoffs: {self.config.config['swarm']['max_handoffs']}")
        print(f"• Max Iterations: {self.config.config['swarm']['max_iterations']}")
        print(f"• Execution Timeout: {self.config.config['swarm']['execution_timeout']}s")

def main():
    """Main function to initialize and run the swarm"""
    try:
        # Initialize the Hynicl multi-agent swarm
        swarm = MultiAgentSwarm()
        
        # Run interactive mode
        swarm.run_interactive_mode()
        
    except Exception as e:
        logger.error(f"Error initializing swarm: {e}")
        print(f"❌ Failed to start Hynicl swarm: {e}")
        print("Make sure Ollama is running and accessible at http://localhost:11434")

def test_swarm():
    """Test function for the swarm"""
    print("🧪 TESTING HYNICL MULTI-AGENT SWARM")
    
    try:
        swarm = MultiAgentSwarm()
        
        test_tasks = [
            "Hello Hynicl, introduce your swarm capabilities",
            "Search for information about local AI models and validate the sources",
            "Calculate compound interest and explain the reasoning behind the formula"
        ]
        
        for task in test_tasks:
            print(f"\n🔬 Testing: {task}")
            result = swarm.execute_task(task)
            print(f"✅ Result: {result}")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_swarm()
    else:
        main()
