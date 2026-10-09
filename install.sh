#!/bin/bash
set -e

echo "=========================================="
echo "Crypto On-chain Analysis Agent - Installer"
echo "=========================================="
echo ""

echo "[1/6] Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "[2/6] Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "[3/6] Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "[4/6] Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file - please configure API keys"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "[5/6] Creating data directory..."
mkdir -p data
echo "✓ Data directory created"

echo ""
echo "[6/6] Verifying installation..."
python -c "import crypto_agent; print('✓ crypto_agent module imports successfully')"

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Configure your .env file with API keys:"
echo "   nano .env"
echo ""
echo "2. Start the API server:"
echo "   source .venv/bin/activate"
echo "   uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "3. Open in browser:"
echo "   http://localhost:8000"
echo ""
echo "4. Test endpoints:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8000/scan"
echo ""
