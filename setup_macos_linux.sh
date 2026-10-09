#!/bin/bash
# Crypto On-chain Analysis Agent - macOS/Linux Auto Setup & Run
# This script does everything automatically

set -e

echo ""
echo "========================================"
echo "Crypto Agent - Auto Setup (macOS/Linux)"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ $PYTHON_VERSION"

echo ""
echo "[1/5] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "[SKIP] Virtual environment already exists"
else
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "[2/5] Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "[3/5] Installing dependencies..."
pip install -q fastapi uvicorn httpx pydantic pydantic-settings python-dotenv apscheduler numpy pandas openai
echo "✓ Dependencies installed"

echo ""
echo "[4/5] Setting up environment file..."
if [ -f ".env" ]; then
    echo "[SKIP] .env file already exists"
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ .env file created from template"
    else
        cat > .env << 'EOF'
OPENAI_API_KEY=
ETHERSCAN_API_KEY=
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=
COINGECKO_API_URL=https://api.coingecko.com/api/v3
LOG_LEVEL=INFO
APP_ENV=development
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DISCORD_WEBHOOK_URL=
EOF
        echo "✓ .env file created with defaults"
    fi
fi

echo ""
echo "[5/5] Creating data directory..."
mkdir -p data
echo "✓ Data directory ready"

echo ""
echo "========================================"
echo "✅ Installation Complete!"
echo "========================================"
echo ""
echo ""
echo "Starting Crypto On-chain Analysis Agent..."
echo ""
echo "ℹ️  API Server: http://localhost:8000"
echo "ℹ️  Swagger Docs: http://localhost:8000/docs"
echo "ℹ️  ReDoc: http://localhost:8000/redoc"
echo "ℹ️  Health Check: http://localhost:8000/health"
echo "ℹ️  Run Scan: http://localhost:8000/scan"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python -m uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
