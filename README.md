# Agentic AI - Basic Project 1

An AI agent implementation using LangChain and AWS Bedrock that can execute multiple tools and maintain conversation memory.

## 📋 Project Overview

This project demonstrates a basic agentic AI system with the following capabilities:

- **LLM Integration**: Uses AWS Bedrock with Amazon Nova Lite model for language understanding
- **Tool Ecosystem**: Extensible tool system supporting Calculator and Weather tools
- **Agent Architecture**: Intelligent agent that decides which tools to use based on user input
- **Memory System**: Maintains conversation history and context
- **Interactive CLI**: User-friendly command-line interface for interaction

## 📁 Project Structure

```
.
├── main.py              # Entry point with interactive CLI
├── config.py            # Configuration settings (model name, max steps)
├── requirements.txt     # Python dependencies
├── agent/               # Agent implementation
│   ├── __init__.py
│   ├── agent.py        # Core agent logic
│   └── memory.py       # Memory management
├── llm/                 # Language Model layer
│   ├── __init__.py
│   ├── base.py         # Base LLM class
│   └── bedrock.py      # AWS Bedrock integration
└── tools/               # Tool implementations
    ├── __init__.py
    ├── base.py         # Base tool class
    ├── calculator.py   # Calculator tool
    ├── weather.py      # Weather tool
    └── registry.py     # Tool registry management
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS Bedrock access (with appropriate credentials configured)
- `pip` or `pipenv` for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agentic-ai/basic-project-1
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure AWS credentials:
   ```bash
   aws configure
   ```

## 💻 Usage

### Interactive Mode

Run the project in interactive mode to chat with the AI agent:

```bash
python main.py
```

Then type your commands at the prompt. Examples:
- `What is the capital of India?`
- `Calculate 25 * 4`
- `What's the weather in New York?`
- Type `exit` to quit

### Programmatic Usage

You can also run the agent directly with specific input:

```python
from agent import Agent
from tools import Calculator, Registry, Weather

registry = Registry()
registry.register(Calculator())
registry.register(Weather())
agent = Agent(tool_registry=registry)

response = agent.run(user_input="What is capital of India?")
```

## ⚙️ Configuration

Edit `config.py` to customize:

- `BEDROCK_MODEL_NAME`: The AWS Bedrock model to use (default: `apac.amazon.nova-lite-v1:0`)
- `MAX_AGENT_STEPS`: Maximum number of iterations the agent can take (default: 10)

## 🔧 Architecture

### Agent
The core agent orchestrates the interaction between the LLM and tools:
- Receives user input
- Queries the LLM to determine which tools to use
- Executes the appropriate tools
- Maintains context and memory
- Returns results to the user

### LLM Layer
Abstraction layer for language models:
- Base LLM interface
- AWS Bedrock implementation
- Extensible for other providers

### Tools System
Pluggable tool system with:
- Base tool interface
- Built-in tools: Calculator, Weather
- Tool registry for discovery and management

### Memory
Conversational memory system that:
- Tracks interaction history
- Maintains context across turns
- Supports multi-turn conversations

## 📦 Dependencies

- **langchain**: LLM framework and orchestration
- **langchain-core**: Core abstractions
- **langchain-openai**: OpenAI integration (dependency chain)
- **langchain-aws**: AWS Bedrock integration
- **rich**: Enhanced terminal output formatting

## 🛠️ Adding New Tools

To add a new tool:

1. Create a new file in `tools/` directory
2. Inherit from the base tool class
3. Register in the tool registry:
   ```python
   from tools import CustomTool
   registry.register(CustomTool())
   ```

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.
