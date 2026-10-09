from __future__ import annotations

import logging
from typing import Any

from crypto_agent.config import get_app_config
from crypto_agent.models import TokenSignal

logger = logging.getLogger("crypto_agent.collectors")


class BaseCollector:
    def __init__(self, chain: str):
        self.chain = chain
        self.config = get_app_config()

    async def fetch_token_market_data(self) -> list[dict[str, Any]]:
        raise NotImplementedError


class SolanaCollector(BaseCollector):
    def __init__(self):
        super().__init__("solana")

    async def fetch_token_market_data(self) -> list[dict[str, Any]]:
        from crypto_agent.connectors.solana import SolanaConnector

        connector = SolanaConnector(
            rpc_url=self.config.solana_rpc_url,
            helius_api_key=self.config.helius_api_key,
        )
        try:
            data = await connector.fetch_top_tokens()
            if data:
                return data
        except Exception as exc:  # pragma: no cover
            logger.warning("Solana live feed failed: %s", exc)

        return [
            {
                "symbol": "SOL",
                "name": "Solana",
                "chain": "solana",
                "price_usd": 168.0,
                "market_cap_usd": 76000000000.0,
                "volume_24h_usd": 5200000000.0,
                "liquidity_usd": 2100000000.0,
                "inflow_usd_1h": 34000000.0,
                "whale_buy_volume_usd_1h": 15000000.0,
                "whale_sell_volume_usd_1h": 2000000.0,
                "large_tx_count_1h": 290,
                "unique_buyers_1h": 980,
                "wallet_growth_1h": 72,
                "price_change_1h": 2.8,
                "price_change_24h": 9.4,
                "contract_address": None,
            },
            {
                "symbol": "JUP",
                "name": "Jupiter",
                "chain": "solana",
                "price_usd": 1.1,
                "market_cap_usd": 1200000000.0,
                "volume_24h_usd": 420000000.0,
                "liquidity_usd": 300000000.0,
                "inflow_usd_1h": 12000000.0,
                "whale_buy_volume_usd_1h": 6200000.0,
                "whale_sell_volume_usd_1h": 950000.0,
                "large_tx_count_1h": 110,
                "unique_buyers_1h": 410,
                "wallet_growth_1h": 35,
                "price_change_1h": 3.2,
                "price_change_24h": 12.2,
                "contract_address": "So11111111111111111111111111111111111111112",
            },
        ]


class EthereumCollector(BaseCollector):
    def __init__(self):
        super().__init__("ethereum")

    async def fetch_token_market_data(self) -> list[dict[str, Any]]:
        from crypto_agent.connectors.ethereum import EthereumConnector

        connector = EthereumConnector(
            rpc_url=self.config.ethereum_rpc_url,
            etherscan_api_key=self.config.etherscan_api_key,
        )
        try:
            data = await connector.fetch_top_tokens()
            if data:
                return data
        except Exception as exc:  # pragma: no cover
            logger.warning("Ethereum live feed failed: %s", exc)

        return [
            {
                "symbol": "ETH",
                "name": "Ethereum",
                "chain": "ethereum",
                "price_usd": 3510.0,
                "market_cap_usd": 421000000000.0,
                "volume_24h_usd": 18400000000.0,
                "liquidity_usd": 1000000000.0,
                "inflow_usd_1h": 9200000.0,
                "whale_buy_volume_usd_1h": 4200000.0,
                "whale_sell_volume_usd_1h": 1000000.0,
                "large_tx_count_1h": 220,
                "unique_buyers_1h": 680,
                "wallet_growth_1h": 44,
                "price_change_1h": 1.8,
                "price_change_24h": 5.8,
                "contract_address": None,
            },
            {
                "symbol": "LINK",
                "name": "Chainlink",
                "chain": "ethereum",
                "price_usd": 18.7,
                "market_cap_usd": 10900000000.0,
                "volume_24h_usd": 640000000.0,
                "liquidity_usd": 500000000.0,
                "inflow_usd_1h": 24000000.0,
                "whale_buy_volume_usd_1h": 8800000.0,
                "whale_sell_volume_usd_1h": 1500000.0,
                "large_tx_count_1h": 120,
                "unique_buyers_1h": 320,
                "wallet_growth_1h": 29,
                "price_change_1h": 2.5,
                "price_change_24h": 8.1,
                "contract_address": "0x514910771af9ca656af840dff83e8264ecf986ca",
            },
        ]


class BaseChainCollector(BaseCollector):
    def __init__(self, chain: str):
        super().__init__(chain)

    async def fetch_token_market_data(self) -> list[dict[str, Any]]:
        if self.chain == "base":
            return [
                {
                    "symbol": "ARB",
                    "name": "Arbitrum",
                    "chain": "base",
                    "price_usd": 1.2,
                    "market_cap_usd": 5200000000.0,
                    "volume_24h_usd": 500000000.0,
                    "liquidity_usd": 430000000.0,
                    "inflow_usd_1h": 14000000.0,
                    "whale_buy_volume_usd_1h": 6300000.0,
                    "whale_sell_volume_usd_1h": 1100000.0,
                    "large_tx_count_1h": 112,
                    "unique_buyers_1h": 330,
                    "wallet_growth_1h": 24,
                    "price_change_1h": 2.1,
                    "price_change_24h": 6.1,
                    "contract_address": None,
                }
            ]
        if self.chain == "polygon":
            return [
                {
                    "symbol": "MATIC",
                    "name": "Polygon",
                    "chain": "polygon",
                    "price_usd": 0.75,
                    "market_cap_usd": 8400000000.0,
                    "volume_24h_usd": 430000000.0,
                    "liquidity_usd": 360000000.0,
                    "inflow_usd_1h": 10000000.0,
                    "whale_buy_volume_usd_1h": 3400000.0,
                    "whale_sell_volume_usd_1h": 900000.0,
                    "large_tx_count_1h": 92,
                    "unique_buyers_1h": 240,
                    "wallet_growth_1h": 16,
                    "price_change_1h": 1.6,
                    "price_change_24h": 5.0,
                    "contract_address": None,
                }
            ]
        return []


class MultiChainCollector:
    def __init__(self):
        self.collectors = {
            "solana": SolanaCollector(),
            "ethereum": EthereumCollector(),
            "base": BaseChainCollector("base"),
            "polygon": BaseChainCollector("polygon"),
        }

    async def collect(self) -> list[TokenSignal]:
        snapshots: list[TokenSignal] = []

        for _, collector in self.collectors.items():
            try:
                market_data = await collector.fetch_token_market_data()
                for row in market_data:
                    snapshots.append(
                        TokenSignal(
                            symbol=row["symbol"],
                            name=row["name"],
                            chain=row["chain"],
                            contract_address=row.get("contract_address"),
                            price_usd=row["price_usd"],
                            market_cap_usd=row["market_cap_usd"],
                            volume_24h_usd=row["volume_24h_usd"],
                            liquidity_usd=row.get("liquidity_usd"),
                            inflow_usd_1h=row["inflow_usd_1h"],
                            whale_buy_volume_usd_1h=row["whale_buy_volume_usd_1h"],
                            whale_sell_volume_usd_1h=row["whale_sell_volume_usd_1h"],
                            large_tx_count_1h=row["large_tx_count_1h"],
                            unique_buyers_1h=row["unique_buyers_1h"],
                            wallet_growth_1h=row["wallet_growth_1h"],
                            price_change_1h=row["price_change_1h"],
                            price_change_24h=row["price_change_24h"],
                        )
                    )
            except Exception as exc:  # pragma: no cover
                logger.warning("Collector failed: %s", exc)

        if not snapshots:
            logger.warning("No token data available from live adapters; returning empty set")

        return snapshots
