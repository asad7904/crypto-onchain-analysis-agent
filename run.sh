#!/bin/bash
set -e

echo "Starting Crypto On-chain Analysis Agent..."
echo ""

source .venv/bin/activate

echo "Running hourly scan scheduler with FastAPI..."
echo "Agent will scan on-chain data every hour."
echo ""
echo "API Server starting on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
