from __future__ import annotations

import asyncio
import logging
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from crypto_agent.collectors import MultiChainCollector
from crypto_agent.engine import SignalEngine

logger = logging.getLogger("crypto_agent.main")

app = FastAPI(title="Crypto On-chain Analysis Agent")
collector = MultiChainCollector()
engine = SignalEngine()
last_scan: list[dict[str, Any]] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/status")
def status() -> dict[str, Any]:
    return {"last_scan_count": len(last_scan), "latest_scan": last_scan[:3]}


@app.get("/scan")
async def scan() -> list[dict[str, Any]]:
    global last_scan
    tokens = await collector.collect()
    ranked = engine.rank_tokens(tokens)
    payload = [signal.model_dump() for signal in ranked]
    last_scan = payload
    return payload


@app.get("/signals")
async def signals() -> list[dict[str, Any]]:
    if not last_scan:
        return await scan()
    return last_scan


def run_scan_sync() -> None:
    asyncio.run(scan())


def start_scheduler() -> None:
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scan_sync, "interval", hours=1, id="hourly_scan")
    scheduler.start()


app.add_event_handler("startup", start_scheduler)
