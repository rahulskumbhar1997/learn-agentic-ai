from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the LLM Client"""

    @abstractmethod
    def invoke(self, messages: list, thread_id: str):
        """Invoke LLM Client"""
