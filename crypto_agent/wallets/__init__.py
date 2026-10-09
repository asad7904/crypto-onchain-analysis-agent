from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger("crypto_agent.connectors.ethereum")


class EthereumConnector:
    def __init__(self, rpc_url: str | None = None, etherscan_api_key: str | None = None):
        self.rpc_url = rpc_url or "https://mainnet.infura.io/v3/YOUR_KEY"
        self.etherscan_api_key = etherscan_api_key

    async def fetch_top_tokens(self) -> list[dict[str, Any]]:
        payload = [
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

        if self.etherscan_api_key:
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    resp = await client.get(
                        "https://api.etherscan.io/api",
                        params={
                            "module": "stats",
                            "action": "tokensupply",
                            "contractaddress": "0x514910771af9ca656af840dff83e8264ecf986ca",
                            "apikey": self.etherscan_api_key,
                        },
                    )
                    resp.raise_for_status()
                    logger.info("Etherscan connector reached successfully")
            except Exception as exc:  # pragma: no cover
                logger.warning("Etherscan request failed: %s", exc)

        if self.rpc_url and "infura" not in self.rpc_url:
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    body = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
                    resp = await client.post(self.rpc_url, json=body)
                    resp.raise_for_status()
                    logger.info("Ethereum RPC reached successfully")
            except Exception as exc:  # pragma: no cover
                logger.warning("Ethereum RPC request failed: %s", exc)

        return payload
