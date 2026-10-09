#!/bin/bash
# One-line installer and starter
# Copy and paste this entire script into your terminal:

set -e
cd crypto-onchain-analysis-agent

echo "🔧 Installing Crypto On-chain Analysis Agent..."
python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
cp .env.example .env
mkdir -p data

echo "✅ Installation complete!"
echo ""
echo "🚀 Starting API server on http://localhost:8000..."
echo ""
echo "To test the agent:"
echo "  1. Open http://localhost:8000/health in browser"
echo "  2. Open http://localhost:8000/scan in browser"
echo "  3. Check http://localhost:8000/docs for API documentation"
echo ""
echo "To configure alerts:"
echo "  nano .env"
echo "  Add TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, or DISCORD_WEBHOOK_URL"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
