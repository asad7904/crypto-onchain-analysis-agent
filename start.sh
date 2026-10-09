#!/bin/bash
set -e

source .venv/bin/activate

echo "🚀 Starting Crypto On-chain Analysis Agent..."
echo ""
echo "📊 API Server: http://localhost:8000"
echo "📖 Swagger Docs: http://localhost:8000/docs"
echo "📍 ReDoc: http://localhost:8000/redoc"
echo ""
echo "Available Endpoints:"
echo "  GET /health       - Health check"
echo "  GET /scan         - Run scan and get top 10 tokens"
echo "  GET /signals      - Get latest scan results"
echo "  GET /top?limit=N  - Get top N tokens"
echo "  GET /status       - Get agent status"
echo "  GET /history      - Get scan history"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
