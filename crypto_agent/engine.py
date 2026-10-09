from __future__ import annotations

import logging
from typing import Iterable

from openai import OpenAI

from crypto_agent.config import get_app_config
from crypto_agent.models import PumpSignal, TokenSignal

logger = logging.getLogger("crypto_agent.engine")


class SignalEngine:
    def __init__(self):
        self.config = get_app_config()
        self.client = OpenAI(api_key=self.config.openai_api_key) if self.config.openai_api_key else None

    def score_token(self, token: TokenSignal) -> PumpSignal:
        score = 0.0
        reasons: list[str] = []

        inflow_score = min(token.inflow_usd_1h / 10_000_000, 25.0)
        score += inflow_score
        if token.inflow_usd_1h > 0:
            reasons.append(f"Net inflow of ${token.inflow_usd_1h:,.0f} over the last hour")

        whale_score = min(token.whale_buy_volume_usd_1h / 5_000_000, 25.0)
        score += whale_score
        if token.whale_buy_volume_usd_1h > 0:
            reasons.append(f"Whale buying volume of ${token.whale_buy_volume_usd_1h:,.0f}")

        tx_score = min(token.large_tx_count_1h / 25.0, 10.0)
        score += tx_score
        if token.large_tx_count_1h > 0:
            reasons.append(f"{token.large_tx_count_1h} large transfers indicate active participation")

        liquidity_score = 0.0
        if token.liquidity_usd is not None:
            liquidity_score = min(token.liquidity_usd / 250_000_000, 15.0)
            score += liquidity_score
            if token.liquidity_usd >= 200_000_000:
                reasons.append("Liquidity remains healthy for continuation")
        else:
            score -= 10.0
            reasons.append("Liquidity data is missing; risk model is more conservative")

        momentum_score = min(max(token.price_change_1h * 10, 0), 8.0)
        score += momentum_score
        if token.price_change_1h > 0:
            reasons.append(f"1h momentum is +{token.price_change_1h:.2f}%")

        risk_penalty = 0.0
        if token.market_cap_usd > 100_000_000_000:
            risk_penalty += 8.0
        if token.liquidity_usd is not None and token.liquidity_usd < 50_000_000:
            risk_penalty += 15.0
        if token.whale_sell_volume_usd_1h > token.whale_buy_volume_usd_1h:
            risk_penalty += 10.0
        score -= risk_penalty

        score = max(0.0, min(score, 100.0))

        if score >= 75:
            risk_level = "low"
        elif score >= 55:
            risk_level = "medium"
        else:
            risk_level = "high"

        probability = 0.35 + score / 170.0
        probability = max(0.0, min(probability, 0.95))

        if self.client and self.config.openai_api_key:
            try:
                liquidity_text = (
                    f"${token.liquidity_usd:,.0f}" if token.liquidity_usd is not None else "$0"
                )
                completion = self.client.responses.create(
                    model="gpt-4o-mini",
                    input=[
                        {
                            "role": "system",
                            "content": "You are a crypto market intelligence assistant. Explain a candidate token's bullish setup in crisp, data-driven language.",
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Token: {token.symbol} on {token.chain}. "
                                f"Inflow 1h: ${token.inflow_usd_1h:,.0f}. "
                                f"Whale buy: ${token.whale_buy_volume_usd_1h:,.0f}. "
                                f"Price 1h: {token.price_change_1h:.2f}%. "
                                f"Liquidity: {liquidity_text}. "
                                f"Large transfers: {token.large_tx_count_1h}. "
                                "Give a concise bullish or cautious explanation."
                            ),
                        },
                    ],
                )
                extra_reason = completion.output_text.strip()
                if extra_reason:
                    reasons.append(extra_reason[:220])
            except Exception as exc:  # pragma: no cover
                logger.warning("OpenAI generation failed: %s", exc)

        return PumpSignal(
            token=token.symbol,
            symbol=token.symbol,
            chain=token.chain,
            score=round(score, 2),
            probability=round(probability, 3),
            risk_level=risk_level,
            reasons=reasons[:5],
            metadata={
                "market_cap_usd": token.market_cap_usd,
                "volume_24h_usd": token.volume_24h_usd,
                "liquidity_usd": token.liquidity_usd,
                "inflow_usd_1h": token.inflow_usd_1h,
                "whale_buy_volume_usd_1h": token.whale_buy_volume_usd_1h,
                "unique_buyers_1h": token.unique_buyers_1h,
            },
        )

    def rank_tokens(self, tokens: Iterable[TokenSignal]) -> list[PumpSignal]:
        signals = [self.score_token(token) for token in tokens]
        return sorted(signals, key=lambda x: x.score, reverse=True)
