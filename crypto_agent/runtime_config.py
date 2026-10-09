from __future__ import annotations

import json
import os

from crypto_agent.config import get_app_config


class MarketConfig:
    def __init__(self):
        self.config = get_app_config()

    def as_dict(self) -> dict[str, str | None]:
        return {
            "openai_api_key": self.config.openai_api_key,
            "etherscan_api_key": self.config.etherscan_api_key,
            "ethereum_rpc_url": self.config.ethereum_rpc_url,
            "solana_rpc_url": self.config.solana_rpc_url,
            "helius_api_key": self.config.helius_api_key,
            "coingecko_api_url": self.config.coingecko_api_url,
            "log_level": self.config.log_level,
            "app_env": self.config.app_env,
        }


def export_runtime_config(path: str = ".runtime-config.json") -> None:
    payload = MarketConfig().as_dict()
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2)
    print(f"Saved runtime config to {path}")


if __name__ == "__main__":
    export_runtime_config()
