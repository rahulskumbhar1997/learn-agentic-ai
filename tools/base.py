
from abc import ABC, abstractmethod

class Tool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool"""

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the tool"""

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """JSON schema which defines the argument for the tool"""

    @abstractmethod
    def execute(self, **kwargs):
        """Actual tool implementation"""

    def to_openai_spec(self) -> dict:
        """Convert this tool to function calling format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }