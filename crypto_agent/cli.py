from __future__ import annotations

import argparse
import asyncio

from crypto_agent.service import SignalAgent


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run a crypto on-chain scan.")
    parser.add_argument("command", choices=["scan", "top"], nargs="?", default="scan")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    agent = SignalAgent()
    if args.command == "scan":
        results = await agent.scan()
    else:
        results = await agent.top_candidates(limit=args.limit)

    print(results[: args.limit])


if __name__ == "__main__":
    asyncio.run(main())
