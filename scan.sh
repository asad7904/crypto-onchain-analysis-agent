#!/bin/bash
set -e

source .venv/bin/activate

echo "Running crypto on-chain scan..."
echo ""

python -m crypto_agent.cli scan --limit 10
