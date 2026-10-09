#!/usr/bin/env python3
"""
Direct Python API for the Crypto On-chain Analysis Agent
Use this to integrate the agent into your own code or scripts.
"""

import asyncio
import logging
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import agent components
try:
    from crypto_agent.service import SignalAgent
    from crypto_agent.storage import SignalStore
    from crypto_agent.engine import SignalEngine
    from crypto_agent.alerts.manager import AlertManager
except ImportError:
    print("❌ crypto_agent module not found. Run: python agent.py")
    exit(1)


class CryptoAgent:
    """High-level API for the crypto analysis agent."""

    def __init__(self):
        self.agent = SignalAgent()
        self.store = SignalStore()
        self.alert_manager = AlertManager()
        logger.info("Crypto Agent initialized")

    async def scan(self, limit: int = 10) -> list[dict[str, Any]]:
        """Run a single on-chain scan."""
        logger.info(f"Running scan for top {limit} tokens")
        results = await self.agent.top_candidates(limit=limit)
        self.store.save_scan(results)
        
        # Alert on high-score signals
        for signal in results[:5]:
            await self.alert_manager.alert_high_score_signal(signal, score_threshold=75.0)
        
        logger.info(f"Scan complete: found {len(results)} candidates")
        return results

    async def get_top_tokens(self, limit: int = 5) -> list[dict[str, Any]]:
        """Get top tokens by pump probability."""
        results = await self.scan(limit=limit)
        return results[:limit]

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """Get scan history from storage."""
        return self.store.load_latest(limit=limit)

    def print_signals(self, signals: list[dict[str, Any]]) -> None:
        """Pretty print signals to console."""
        if not signals:
            print("No signals available")
            return

        print("\n" + "="*100)
        print(f"{'Symbol':<10} {'Chain':<12} {'Score':<8} {'Probability':<12} {'Risk':<8} {'Inflow 1h':<15}")
        print("="*100)

        for signal in signals:
            symbol = signal.get("symbol", "N/A")
            chain = signal.get("chain", "N/A")
            score = signal.get("score", 0)
            prob = signal.get("probability", 0)
            risk = signal.get("risk_level", "N/A")
            inflow = signal.get("metadata", {}).get("inflow_usd_1h", 0)

            print(f"{symbol:<10} {chain:<12} {score:<8.2f} {prob:<12.1%} {risk:<8} ${inflow:<14,.0f}")

        print("="*100 + "\n")


async def main():
    """Example usage of the crypto agent."""
    agent = CryptoAgent()

    # Run a scan
    print("\n🔍 Running On-chain Scan...\n")
    signals = await agent.scan(limit=10)

    # Display results
    print("\n📊 Top Pump Candidates:\n")
    agent.print_signals(signals[:5])

    # Show detailed info for top signal
    if signals:
        top = signals[0]
        print(f"\n🎯 Top Signal: {top['symbol']} on {top['chain']}")
        print(f"   Score: {top['score']}/100")
        print(f"   Probability: {top['probability']:.1%}")
        print(f"   Risk Level: {top['risk_level'].upper()}")
        print(f"   Reasons:")
        for reason in top.get('reasons', [])[:3]:
            print(f"     • {reason}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Crypto On-chain Analysis Agent - Direct API")
    print("="*60 + "\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutdown requested.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
