# 🤖 HYNICL Multi-Agent Swarm System

A sophisticated multi-agent system powered by local Ollama models that coordinates specialized AI agents to solve complex tasks collaboratively. The system features a master coordinator (HYNICL) that orchestrates specialist agents for search, reasoning, tool operations, and validation.

## 🌟 Features

- **🎯 Master Coordination**: HYNICL agent serves as both coordinator and specialist
- **🔧 Specialized Agents**: Search, Reasoning, Tool, and Validation specialists
- **🏠 Local AI**: Runs entirely on local Ollama models (privacy-first)
- **⚡ Real-time Processing**: Asynchronous task execution with swarm intelligence
- **🔄 Dynamic Handoffs**: Intelligent agent-to-agent task delegation
- **📊 Comprehensive Logging**: Detailed execution tracking and metrics
- **🛡️ Error Recovery**: Robust error handling and graceful degradation
- **📋 24/7 Operation**: Designed for continuous task processing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HYNICL MASTER AGENT                     │
│              (Coordinator + Specialist)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌────▼────┐ ┌──────▼──────┐ ┌──────────▼───────┐
│   SEARCH     │ │REASONING│ │    TOOL     │ │   VALIDATION     │
│   AGENT      │ │ AGENT   │ │   AGENT     │ │     AGENT        │
│              │ │         │ │             │ │                  │
│• Web Search  │ │• Logic  │ │• File Ops   │ │• Quality Check   │
│• Info Gather │ │• Analysis│ │• Code Exec  │ │• Verification    │
│• Data Retriev│ │• Decision│ │• Technical  │ │• Standards       │
└──────────────┘ └─────────┘ └─────────────┘ └──────────────────┘
```

### Agent Roles

- **🎯 HYNICL (Master)**: Orchestrates tasks, makes executive decisions, provides specialized analysis
- **🔍 Search Agent**: Handles web searches, information retrieval, and data gathering
- **🧠 Reasoning Agent**: Performs logical analysis, decision-making, and complex reasoning
- **🔧 Tool Agent**: Manages file operations, code execution, and technical implementations
- **✅ Validation Agent**: Ensures quality assurance, verification, and standards compliance

## 📋 Prerequisites

- **Python 3.8+**
- **Ollama** installed and running locally
- **Virtual environment** (recommended)

## ⚙️ Installation

### 1. Install Ollama

First, install Ollama on your system:

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or visit https://ollama.ai for other installation methods
```

### 2. Download and Run a Model

```bash
# Download a model (e.g., llama3.2:1b for lightweight operation)
ollama pull llama3.2:1b

# Start Ollama server
ollama serve
```

### 3. Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd multi-agent-swarm

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Should return available models including llama3.2:1b
```

## 🚀 Quick Start

### Running the Swarm

```bash
# Navigate to agents directory
cd agents

# Start the interactive swarm
python main.py

# For testing mode
python main.py test
```

### Interactive Mode

Once started, you'll see the interactive interface:

```
======================================================================
🤖 HYNICL MULTI-AGENT SWARM WITH OLLAMA 🤖
======================================================================
🎯 Master Coordinator: HYNICL
🔧 Specialists: search, reasoning, tool, validation
🏠 Local AI: llama3.2:1b
======================================================================
💡 Type 'help' for commands, 'quit' to exit
The Hynicl master will coordinate specialists to solve your tasks!
======================================================================

🎯 Task: 
```

### Example Tasks

```bash
# Simple greeting
🎯 Task: Hello, introduce your capabilities

# Complex research task
🎯 Task: Research quantum computing principles and create a technical summary

# Multi-step analysis
🎯 Task: Analyze the Python code in this directory and suggest improvements

# File operations
🎯 Task: Create a data analysis script and execute it with sample data

# Validation workflow
🎯 Task: Search for AI best practices, analyze them, and validate the information
```

### Available Commands

- `help` - Show available commands and examples
- `agents` - Display agent roles and capabilities
- `config` - Show current system configuration
- `quit` / `exit` - Shutdown the swarm

## ⚙️ Configuration

The system is configured via `config.yml`:

```yaml
ollama:
  host: http://localhost:11434
  default_model: llama3.2:1b
  temperature: 0.7
  keep_alive: 10m

swarm:
  max_handoffs: 25
  max_iterations: 30
  execution_timeout: 1200.0
  node_timeout: 300.0
  repetitive_handoff_detection_window: 8
  repetitive_handoff_min_unique_agents: 3

Prompt:
  # Agent-specific system prompts
  hynicl_agent_prompt: |
    # Master coordinator prompt
  # ... other agent prompts
```

### Key Configuration Options

- **max_handoffs**: Maximum agent-to-agent task handoffs
- **max_iterations**: Maximum processing iterations per task
- **execution_timeout**: Total task timeout (seconds)
- **node_timeout**: Per-agent timeout (seconds)
- **temperature**: Model creativity level (0.0-1.0)

## 🛠️ Project Structure

```
multi-agent-swarm/
├── agents/                     # Core agent implementations
│   ├── __init__.py            # Package initialization
│   ├── base.py                # Base classes and utilities
│   ├── hynicl_agent.py        # Master coordinator agent
│   ├── search_agent.py        # Search specialist
│   ├── reasoning_agent.py     # Reasoning specialist
│   ├── tool_agent.py          # Tool specialist
│   ├── validation_agent.py    # Validation specialist
│   └── main.py                # Main application entry
├── simulator/                  # 24/7 operation simulator
│   └── twenty_four_seven.py   # Continuous operation logic
├── config.yml                 # System configuration
├── requirements.txt           # Python dependencies
├── commands.csv               # Command history/templates
├── TODO                       # Development roadmap
└── README.md                  # This file
```

### Core Components

- **BaseAgent**: Abstract base class for all agents
- **SwarmConfig**: Configuration management
- **OllamaClient**: Enhanced Ollama API client
- **Multi-Agent Tools**: Shared tools for file operations, calculations, etc.

## 🔧 Advanced Usage

### Custom Agent Development

Create new specialist agents by extending `BaseAgent`:

```python
from base import BaseAgent
from strands import Agent
from strands_tools import memory

class CustomAgent(BaseAgent):
    def __init__(self, ollama_model):
        super().__init__("custom", ollama_model)
    
    def create_agent(self) -> Agent:
        return Agent(
            name=self.name,
            model=self.ollama_model,
            system_prompt="Your custom prompt here",
            tools=[memory, ...]
        )

def create_custom_agent(ollama_model):
    return CustomAgent(ollama_model).get_agent()
```

### Task Automation

For 24/7 operation, use the simulator:

```python
# In simulator/twenty_four_seven.py
from agents.main import MultiAgentSwarm

swarm = MultiAgentSwarm()
# Implement continuous task processing logic
```

### Integration with External Systems

The swarm can be integrated with external systems via APIs:

```python
from agents.main import MultiAgentSwarm

# Initialize swarm
swarm = MultiAgentSwarm()

# Process external task
result = swarm.execute_task("Process this external request")
print(f"Result: {result}")
```

## 📊 Monitoring and Logging

The system provides comprehensive logging:

- **INFO**: General operation status
- **DEBUG**: Detailed swarm execution flow
- **ERROR**: Error conditions and recovery

Logs include:
- Agent handoffs and coordination
- Task execution metrics
- Performance statistics
- Error diagnostics

## 🔍 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Check model availability
   ollama list
   ```

2. **Import Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   
   # Check Python path
   python -c "import strands; print('Success')"
   ```

3. **Configuration Issues**
   ```bash
   # Validate config file
   python -c "import yaml; yaml.safe_load(open('config.yml'))"
   ```

4. **Agent Execution Failures**
   - Check system prompts are strings (not lists)
   - Verify agent tool compatibility
   - Monitor timeout settings

### Performance Optimization

- **Model Selection**: Use lighter models (llama3.2:1b) for faster response
- **Timeout Tuning**: Adjust timeouts based on task complexity
- **Memory Management**: Monitor system resources during long-running tasks
- **Handoff Limits**: Tune max_handoffs to prevent infinite loops

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Follow Python PEP 8 style guidelines
- Add docstrings for new functions/classes
- Update configuration examples
- Test with multiple Ollama models

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama Team** for local AI model infrastructure
- **Strands Framework** for multi-agent coordination
- **Community Contributors** for testing and feedback

## 🔮 Roadmap

- [ ] **Enhanced Observability**: Real-time monitoring dashboard
- [ ] **Task Scheduling**: Cron-like task automation
- [ ] **Agent Marketplace**: Pluggable specialist agents
- [ ] **Performance Analytics**: Detailed metrics and insights
- [ ] **Web Interface**: Browser-based interaction
- [ ] **API Gateway**: RESTful API for external integration
- [ ] **Docker Deployment**: Containerized deployment options

---

**Built with ❤️ for the AI community**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/your-username/multi-agent-swarm).



# test agent run 