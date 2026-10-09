from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass(frozen=True)
class AppConfig:
    openai_api_key: str | None
    etherscan_api_key: str | None
    ethereum_rpc_url: str | None
    solana_rpc_url: str | None
    helius_api_key: str | None
    coingecko_api_url: str | None
    log_level: str
    app_env: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = None
    etherscan_api_key: str | None = None
    ethereum_rpc_url: str | None = None
    solana_rpc_url: str | None = None
    helius_api_key: str | None = None
    coingecko_api_url: str = "https://api.coingecko.com/api/v3"
    log_level: str = "INFO"
    app_env: str = "development"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_app_config() -> AppConfig:
    settings = get_settings()
    return AppConfig(
        openai_api_key=settings.openai_api_key,
        etherscan_api_key=settings.etherscan_api_key,
        ethereum_rpc_url=settings.ethereum_rpc_url,
        solana_rpc_url=settings.solana_rpc_url,
        helius_api_key=settings.helius_api_key,
        coingecko_api_url=settings.coingecko_api_url,
        log_level=settings.log_level,
        app_env=settings.app_env,
    )
