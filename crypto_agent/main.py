from __future__ import annotations

import logging
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from crypto_agent.service import SignalAgent
from crypto_agent.storage import SignalStore

logger = logging.getLogger("crypto_agent.main")

app = FastAPI(title="Crypto On-chain Analysis Agent")
agent = SignalAgent()
store = SignalStore()
last_scan: list[dict[str, Any]] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/status")
def status() -> dict[str, Any]:
    return {
        "last_scan_count": len(last_scan),
        "latest_scan": last_scan[:3],
        "stored_scan_count": store.count_scans(),
    }


@app.get("/scan")
async def scan(limit: int = 10) -> list[dict[str, Any]]:
    global last_scan
    results = await agent.top_candidates(limit=limit)
    store.save_scan(results)
    last_scan = results
    return results


@app.get("/signals")
async def signals(limit: int = 10) -> list[dict[str, Any]]:
    if not last_scan:
        return await scan(limit=limit)
    return last_scan[:limit]


@app.get("/top")
async def top(limit: int = 10) -> list[dict[str, Any]]:
    return await scan(limit=limit)


def run_scan_sync() -> None:
    import asyncio

    asyncio.run(scan(limit=10))


def start_scheduler() -> None:
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scan_sync, "interval", hours=1, id="hourly_scan")
    scheduler.start()


app.add_event_handler("startup", start_scheduler)
