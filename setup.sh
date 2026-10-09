#!/bin/bash
set -e

echo "=================================="
echo "Crypto On-chain Analysis Agent"
echo "=================================="
echo ""

echo "Step 1: Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "Step 3: Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "Step 4: Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file (configure API keys as needed)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "Step 5: Creating data directory..."
mkdir -p data
echo "✓ Data directory ready"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To run the API server, execute:"
echo "  uvicorn crypto_agent.main:app --reload"
echo ""
echo "To run a single scan via CLI, execute:"
echo "  python -m crypto_agent.cli scan --limit 10"
echo ""
echo "API will be available at:"
echo "  http://localhost:8000"
echo ""
echo "API Endpoints:"
echo "  GET  /health          - Health check"
echo "  GET  /scan            - Run scan and get top 10 tokens"
echo "  GET  /signals         - Get latest scan results"
echo "  GET  /top?limit=5     - Get top N tokens"
echo "  GET  /status          - Get agent status"
echo ""
