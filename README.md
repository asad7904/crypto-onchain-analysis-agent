# Crypto On-chain Analysis Agent

A production-minded AI agent that scans major on-chain ecosystems every hour and ranks tokens most likely to pump based on net inflow, whale buying pressure, liquidity health, momentum, and risk filters.

Features:
- Multi-chain coverage: Ethereum, Solana, Base, Polygon, and extensible ecosystem adapters
- Hourly scanning scheduler
- Whale activity and inflow detection
- Risk-adjusted ranking to prioritize likely momentum plays
- AI-generated explanation layer using OpenAI when configured
- FastAPI API for dashboard integration and alerts
- Fallback demo mode for local testing without keys

Architecture:
- Collectors obtain market and on-chain context from public APIs and blockchain RPC endpoints
- Normalizer standardizes signals across chains
- Signal engine scores candidates with a transparent, explainable formula
- Reasoning layer turns raw numbers into human-readable insights

Quick start:

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   ```

4. Run the API:
   ```bash
   uvicorn crypto_agent.main:app --reload
   ```

5. Query the agent:
   ```bash
   curl http://localhost:8000/scan
   curl http://localhost:8000/signals
   ```

Core endpoints:
- GET /health
- GET /scan
- GET /signals
- GET /status

Signal scoring logic:
- Net inflow and large transfer volume receive the highest weight
- Whale buy pressure is treated as a strong acceleration signal
- Fresh money and wallet growth are favored if liquidity remains healthy
- Very low-liquidity, concentrated, or high-volatility setups are down-ranked
- The final score is risk-adjusted so the output is actionable but cautious

Recommended production upgrades:
- Replace mock token universe with real DEX/bridge event ingestion from Helius, Etherscan, and The Graph
- Add PostgreSQL + TimescaleDB for historical signal storage
- Add stream ingestion and queue workers for sub-hour latency
- Add alert destinations (Discord, Telegram, Slack)
- Add model retraining with labeled historical bull-runs to improve ranking quality

This project is intentionally designed to be extensible. The on-chain connectors are modular, so you can add Arbitrum, BNB Chain, Blast, Avalanche, or any EVM chain without rewriting the core scoring engine.
