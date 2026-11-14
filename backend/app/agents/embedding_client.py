"""Embedding client interface with deterministic Mock implementation."""
from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod


class EmbeddingClient(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass


class MockEmbeddingClient(EmbeddingClient):
    """Deterministic mock embedding generating normalized 1536-dim vector from sha256."""

    async def embed(self, text: str) -> list[float]:
        # Generate pseudo-random deterministic floats from text hash
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vec: list[float] = []
        for i in range(1536):
            b = h[i % len(h)]
            vec.append((b / 255.0) - 0.5)
        # Normalize
        norm = sum(x * x for x in vec) ** 0.5 or 1.0
        return [round(x / norm, 5) for x in vec]


def get_embedding_client() -> EmbeddingClient:
    return MockEmbeddingClient()
