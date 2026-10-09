from __future__ import annotations

from typing import Any


class WalletClusterer:
    def __init__(self):
        self.exchange_labels = {
            "binance": "exchange",
            "coinbase": "exchange",
            "kraken": "exchange",
            "bybit": "exchange",
            "okx": "exchange",
        }

    def cluster(self, wallets: list[dict[str, Any]]) -> list[dict[str, Any]]:
        clusters: list[dict[str, Any]] = []
        for wallet in wallets:
            label = wallet.get("label", "unknown").lower()
            cluster_type = self.exchange_labels.get(label, "wallet")
            clusters.append({
                "address": wallet.get("address"),
                "label": wallet.get("label", "unknown"),
                "type": cluster_type,
                "balance_usd": wallet.get("balance_usd", 0.0),
            })
        return clusters

    def detect_whale_clusters(self, wallets: list[dict[str, Any]], threshold_usd: float = 1_000_000.0) -> list[dict[str, Any]]:
        large_wallets = [w for w in self.cluster(wallets) if w["balance_usd"] >= threshold_usd]
        return large_wallets
