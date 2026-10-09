from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from crypto_agent.collectors import MultiChainCollector
from crypto_agent.engine import SignalEngine


@dataclass
class SignalAgent:
    collector: MultiChainCollector = field(default_factory=MultiChainCollector)
    engine: SignalEngine = field(default_factory=SignalEngine)

    async def scan(self) -> list[dict[str, Any]]:
        tokens = await self.collector.collect()
        ranked = self.engine.rank_tokens(tokens)
        return [signal.model_dump() for signal in ranked]

    async def top_candidates(self, limit: int = 10) -> list[dict[str, Any]]:
        results = await self.scan()
        return results[:limit]
