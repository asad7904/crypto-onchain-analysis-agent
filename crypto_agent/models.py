from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class TokenSignal(BaseModel):
    symbol: str
    name: str
    chain: str
    contract_address: str | None = None
    price_usd: float = 0.0
    market_cap_usd: float = 0.0
    volume_24h_usd: float = 0.0
    liquidity_usd: float | None = None
    inflow_usd_1h: float = 0.0
    whale_buy_volume_usd_1h: float = 0.0
    whale_sell_volume_usd_1h: float = 0.0
    large_tx_count_1h: int = 0
    unique_buyers_1h: int = 0
    wallet_growth_1h: int = 0
    price_change_1h: float = 0.0
    price_change_24h: float = 0.0
    confidence: float = 0.0


class PumpSignal(BaseModel):
    token: str
    symbol: str
    chain: str
    score: float = Field(..., ge=0.0, le=100.0)
    probability: float = Field(..., ge=0.0, le=1.0)
    risk_level: Literal["low", "medium", "high"]
    reasons: list[str] = []
    metadata: dict = {}
