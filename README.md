# Agentic AI - Basic Project 1

An AI agent implementation using LangChain and AWS Bedrock that can execute multiple tools and maintain conversation memory.

## 📋 Project Overview

This project demonstrates a basic agentic AI system with the following capabilities:

- **LLM Integration**: Uses AWS Bedrock with Amazon Nova Lite model for language understanding
- **Tool Ecosystem**: Extensible tool system with Calculator, Weather, and Web Search tools
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
   ├── web_search.py   # Tavily-powered web search tool
   └── registry.py     # Tool registry management
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- AWS Bedrock access (with Bedrock API key configured)
- Tavily API key for web search tool
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

4. Configure environment variables (required before running `main.py`):

   macOS/Linux:
   ```bash
   export AWS_BEARER_TOKEN_BEDROCK="your_bedrock_api_key"
   export AWS_REGION_NAME="ap-south-1"
   export TAVILY_API_KEY="your_tavily_api_key"
   ```

   Windows PowerShell:
   ```powershell
   $env:AWS_BEARER_TOKEN_BEDROCK="your_bedrock_api_key"
   $env:AWS_REGION_NAME="ap-south-1"
   $env:TAVILY_API_KEY="your_tavily_api_key"
   ```

   Notes:
   - This setup uses Bedrock API key authentication via `AWS_BEARER_TOKEN_BEDROCK`.
   - Region defaults to `ap-south-1` in `config.py`, but setting `AWS_REGION_NAME` explicitly is recommended.

## 💻 Usage

### Interactive Mode

Run the project in interactive mode to chat with the AI agent:

```bash
python main.py
```

Then type your commands at the prompt. Examples:
- `What is the capital of India?`
- `Calculate 25 * 4`
- `What is the weather current weather in Pune?`
- `Search latest AI news`
- Type `exit` to quit


## ⚙️ Configuration

Edit `config.py` to customize:

- `BEDROCK_MODEL_NAME`: The AWS Bedrock model to use (default: `apac.amazon.nova-lite-v1:0`)
- `MAX_AGENT_STEPS`: Maximum number of iterations the agent can take (default: 10)
- `AWS_REGION_NAME`: AWS region used by Bedrock client (default: `ap-south-1`)

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
- Built-in tools: Calculator, Weather, Web Search (Tavily)
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
- **tavily-python**: Web search integration

## 🛠️ Adding New Tools

To add a new tool:

1. Create a new file in `tools/` directory
2. Inherit from the base tool class
3. Register in the tool registry:
   ```python
   from tools import CustomTool
   registry.register(CustomTool())
   ```
