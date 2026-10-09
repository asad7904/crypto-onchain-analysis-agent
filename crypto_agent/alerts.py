from __future__ import annotations

import json
import os
from typing import Any

import httpx


class SignalAlertDispatcher:
    def __init__(self, telegram_token: str | None = None, telegram_chat_id: str | None = None, discord_webhook_url: str | None = None):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.discord_webhook_url = discord_webhook_url

    def send(self, signal: dict[str, Any]) -> None:
        message = (
            f"{signal.get('symbol')} | {signal.get('chain')} | "
            f"score={signal.get('score')} | probability={signal.get('probability')}\n"
            f"reasons={signal.get('reasons', [])[:2]}"
        )

        if self.telegram_token and self.telegram_chat_id:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {"chat_id": self.telegram_chat_id, "text": message, "parse_mode": "HTML"}
            try:
                httpx.post(url, json=payload, timeout=10)
            except Exception:
                pass

        if self.discord_webhook_url:
            try:
                httpx.post(self.discord_webhook_url, json={"content": message}, timeout=10)
            except Exception:
                pass


class AlertManager:
    def __init__(self):
        self.dispatcher = SignalAlertDispatcher(
            telegram_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            discord_webhook_url=os.getenv("DISCORD_WEBHOOK_URL"),
        )

    def notify_top_signal(self, signal: dict[str, Any]) -> None:
        self.dispatcher.send(signal)
