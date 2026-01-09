"""
AI service for processing natural language text.
Prepared for LLM integration (OpenAI, Anthropic, etc.)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from app.core.logging import logger


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def parse_task(self, text: str) -> Dict[str, Any]:
        """
        Parse task information from natural language text.

        Args:
            text: Natural language text describing the task

        Returns:
            Dictionary with extracted task information
        """
        pass


class MockLLMProvider(BaseLLMProvider):
    """
    Mock LLM provider for testing.
    Uses simple rule-based extraction.
    """

    async def parse_task(self, text: str) -> Dict[str, Any]:
        """
        Parse task using simple rules (placeholder for real LLM).

        Args:
            text: Natural language text

        Returns:
            Extracted task data
        """
        logger.info("Parsing task with mock LLM")

        # TODO: Implement actual parsing logic
        return {
            "summary": text[:100] if len(text) > 100 else text,
            "description": text,
            "priority": "Medium",
            "issue_type": "Task",
            "confidence": 0.75
        }


class AIService:
    """
    Service for AI-powered text processing.
    """

    def __init__(self, provider: BaseLLMProvider = None):
        """
        Initialize AI service with LLM provider.

        Args:
            provider: LLM provider instance (defaults to MockLLMProvider)
        """
        self.provider = provider or MockLLMProvider()
        logger.info(f"AI Service initialized with {type(self.provider).__name__}")

    async def parse_task_from_text(self, text: str) -> Dict[str, Any]:
        """
        Parse task information from natural language text.

        Args:
            text: Natural language description of the task

        Returns:
            Dictionary with extracted task information
        """
        # TODO: Add validation and error handling
        result = await self.provider.parse_task(text)
        return result


# TODO: Implement OpenAI provider
class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider (to be implemented)."""

    async def parse_task(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError("OpenAI provider not yet implemented")


# TODO: Implement Anthropic provider
class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM provider (to be implemented)."""

    async def parse_task(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError("Anthropic provider not yet implemented")
