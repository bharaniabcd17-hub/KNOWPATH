"""LLM Client interface with deterministic Mock implementation and Anthropic adapter."""
from __future__ import annotations

import hashlib
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel


class LLMMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str


class LLMResponse(BaseModel):
    content: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    model: str
    is_mock: bool = False


class LLMClient(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[LLMMessage],
        system: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> LLMResponse:
        pass


class MockLLMClient(LLMClient):
    """Deterministic, label-explicit mock LLM for testing and local execution without API keys."""

    async def complete(
        self,
        messages: list[LLMMessage],
        system: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> LLMResponse:
        last_msg = messages[-1].content if messages else ""

        # Deterministic generation based on system prompt / context
        if "Teaching Agent" in (system or "") or "explain" in last_msg.lower():
            content = (
                "🤖 [AI-Generated Explanation - Mock Adapter]\n\n"
                "In Python, this concept is grounded directly in the official language semantics. "
                "Understanding the underlying object references and memory models prevents common errors. "
                "Always verify your assumptions using the interactive Python interpreter.\n\n"
                "Sources cited: concept materials stored in Knowledge Genome."
            )
        elif "Draft Question" in last_msg or "Assessment Agent" in (system or ""):
            content = (
                '{\n'
                '  "stem": "What is the expected output of x = [1, 2]; y = x; y.append(3); print(len(x))?",\n'
                '  "options": {"A": "2", "B": "3", "C": "Error", "D": "None"},\n'
                '  "correct": "B",\n'
                '  "explanation": "Lists are mutable objects in Python. Reassignment binds y to the same object in memory as x.",\n'
                '  "difficulty": 0.35,\n'
                '  "discrimination": 0.65\n'
                '}'
            )
        else:
            content = (
                "🤖 [AI-Generated Response - PROJECT-EVOLVE Mock Adapter]\n"
                "This output is deterministically generated for offline verification."
            )

        tokens_in = sum(len(m.content.split()) for m in messages)
        tokens_out = len(content.split())
        # Cost estimate: $0.000003 per token
        cost = round((tokens_in + tokens_out) * 0.000003, 6)

        return LLMResponse(
            content=content,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost,
            model="mock-claude-3-5-sonnet",
            is_mock=True,
        )


class AnthropicLLMClient(LLMClient):
    """Real Anthropic Claude implementation."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        import anthropic

        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model

    async def complete(
        self,
        messages: list[LLMMessage],
        system: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> LLMResponse:
        import anthropic

        formatted_msgs = [{"role": m.role, "content": m.content} for m in messages if m.role != "system"]
        res = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "",
            messages=formatted_msgs,
        )
        content = res.content[0].text if res.content else ""
        tokens_in = res.usage.input_tokens
        tokens_out = res.usage.output_tokens
        cost = (tokens_in * 0.000003) + (tokens_out * 0.000015)

        return LLMResponse(
            content=f"🤖 [AI-Generated]\n{content}",
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=round(cost, 6),
            model=self.model,
            is_mock=False,
        )


def get_llm_client() -> LLMClient:
    from app.config import get_settings

    cfg = get_settings()
    if cfg.llm_provider == "anthropic" and cfg.anthropic_api_key and cfg.anthropic_api_key != "your-anthropic-key":
        return AnthropicLLMClient(api_key=cfg.anthropic_api_key)
    return MockLLMClient()
