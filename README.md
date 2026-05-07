# Agentic AI

A multi-provider AI agent implementation using LangChain/LangGraph with tool calling, MCP (Model Context Protocol) integrations, and conversational memory.

## 📋 Project Overview

This project demonstrates an agentic AI system featuring:

- **Multi-Provider LLM Support**: AWS Bedrock (Amazon Nova Lite) and Azure OpenAI (GPT-4.1-mini)
- **LangGraph Agents**: Intelligent agents with built-in memory using LangGraph's `create_agent`
- **Native Tools**: Weather forecasts (Open-Meteo) and web search (Tavily)
- **MCP Integrations**: External tool servers for travel (Kiwi.com) and sports (cricket data)
- **LangSmith Tracing**: Full observability for LLM calls, tool executions, and agent runs
- **Interactive CLI**: Rich markdown-formatted responses in the terminal

## 📁 Project Structure

```
.
├── main.py              # Entry point with interactive CLI
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── llm/                 # LLM provider implementations
│   ├── __init__.py
│   ├── base.py          # Abstract base class for LLM clients
│   ├── bedrock.py       # AWS Bedrock integration
│   └── azure_foundry.py # Azure OpenAI integration
├── tools/               # Native LangChain tools
│   ├── __init__.py
│   ├── weather.py       # Open-Meteo weather API
│   └── web_search.py    # Tavily web search
└── mcp_clients/         # MCP (Model Context Protocol) clients
    ├── __init__.py
    ├── travel.py        # Kiwi.com travel/flights MCP
    └── sports.py        # Cricket sports data MCP
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Tavily API key (for web search)
- Azure OpenAI credentials (if using Azure) or AWS credentials (if using Bedrock)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd learn-agentic-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (see `.env.example`) with your credentials:
   ```env
   # LangSmith (for tracing and observability)
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_PROJECT=your_project_name

   # Tavily (required for web search)
   TAVILY_API_KEY=your_tavily_api_key

   # Azure OpenAI (default provider)
   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_API_VERSION=your_api_version

   # AWS Bedrock (alternative provider)
   AWS_BEARER_TOKEN_BEDROCK=your_bedrock_token
   ```

## Usage

Run the interactive CLI:

```bash
python main.py
```

Example queries:
- `What's the weather in Tokyo?`
- `Search for latest news on AI`
- `Find flights from New York to London`
- `What are the upcoming cricket matches?`
- Type `exit` to quit


## ⚙️ Configuration

Edit `config.py` to customize:

```python
# AWS Bedrock settings
BEDROCK_MODEL = "apac.amazon.nova-lite-v1:0"
BEDROCK_REGION = "ap-south-1"

# Azure OpenAI settings
AZURE_DEPLOYMENT_NAME = "gpt-4.1-mini"
AZURE_DEPLOYMENT_API_VERSION = "2025-01-01-preview"
```

To switch LLM providers, modify `main.py`:
```python
# Use Azure OpenAI (default)
llm_client = AzureFoundry(tools=tools)

# Or use AWS Bedrock
# llm_client = BedRock(tools=tools)
```

## Architecture

### LLM Layer

Abstract base class (`BaseLLM`) with implementations for:
- **AzureFoundry**: Azure OpenAI with GPT-4.1-mini
- **BedRock**: AWS Bedrock with Amazon Nova Lite

Both use LangGraph's `create_agent` with `InMemorySaver` for conversation memory.

### Tools

Native LangChain tools decorated with `@tool`:
- **get_weather**: Fetches weather data from Open-Meteo API (supports current, hourly, and daily forecasts)
- **web_search**: Performs web searches using Tavily

### MCP Clients

Model Context Protocol integrations using `langchain-mcp-adapters`:
- **TravelMCP**: Flight search and travel info via Kiwi.com
- **SportsMCP**: Cricket match data via whensport.com

## 📊 LangSmith Tracing

This project integrates [LangSmith](https://smith.langchain.com/) for comprehensive observability of your AI agent.

### What Gets Traced

- **LLM Calls**: Every request/response to Azure OpenAI or AWS Bedrock
- **Tool Executions**: Input/output of weather, web search, and MCP tools
- **Agent Runs**: Full execution flow including reasoning steps and tool selections
- **Token Usage**: Track token consumption and costs per request
- **Latency Metrics**: Response times for each component

### Setup

1. Create a free account at [smith.langchain.com](https://smith.langchain.com/)
2. Create a new project and copy your API key
3. Add the following to your `.env` file:
   ```env
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_api_key
   LANGSMITH_PROJECT=your_project_name
   ```

### Viewing Traces

Once configured, all agent interactions are automatically logged. Visit [smith.langchain.com](https://smith.langchain.com/) to:

- View detailed execution traces for each conversation
- Debug tool call failures and LLM responses
- Analyze latency and token usage patterns
- Compare runs across different prompts or configurations

> **Note**: Set `LANGSMITH_TRACING=false` to disable tracing in production or for privacy.

## Adding New Components

### New Tool

Create a file in `tools/` and use the `@tool` decorator:

```python
from langchain.tools import tool

@tool(description="Description of what your tool does")
def my_tool(param: str) -> str:
    """Tool docstring."""
    # Implementation
    return result
```

Export it in `tools/__init__.py` and add to the tools list in `main.py`.

### New MCP Client

Create a file in `mcp_clients/`:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

class MyMCP:
    def __init__(self):
        self._client = MultiServerMCPClient({
            "server_name": {
                "url": "https://mcp-server-url",
                "transport": "streamable_http"
            }
        })

    async def get_tools(self):
        return await self._client.get_tools()
```

### New LLM Provider

Create a file in `llm/` inheriting from `BaseLLM`:

```python
from .base import BaseLLM
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

class MyProvider(BaseLLM):
    def __init__(self, tools=None):
        self._llm = # Initialize your LangChain chat model
        self._agent = create_agent(self._llm, tools=tools, checkpointer=InMemorySaver())

    def name(self) -> str:
        return "my_provider"

    async def invoke(self, messages: list, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        return await self._agent.ainvoke({"messages": messages}, config=config)
```

## Dependencies

| Package | Purpose |
|---------|---------|
| langchain | LLM framework and orchestration |
| langchain-aws | AWS Bedrock integration |
| langchain-openai | Azure OpenAI integration |
| langchain-mcp-adapters | MCP client support |
| langgraph | Agent creation with memory |
| langsmith | Tracing and observability |
| tavily-python | Web search API |
| rich | Terminal markdown formatting |
| python-dotenv | Environment variable management |
