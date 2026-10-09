# Crypto On-chain Analysis Agent - Installation Guide

## Quick Start (Copy & Paste)

### Step 1: Clone and Navigate
```bash
cd crypto-onchain-analysis-agent
```

### Step 2: One-Command Install & Run

**On macOS or Linux:**
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -q -r requirements.txt && cp .env.example .env && mkdir -p data && uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -q -r requirements.txt; copy .env.example .env; mkdir -Force data; uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
```

**On Windows (CMD):**
```cmd
python -m venv .venv && .venv\Scripts\activate.bat && pip install -q -r requirements.txt && copy .env.example .env && mkdir data && uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Step-by-Step Installation

### 1. Create Virtual Environment
```bash
python3 -m venv .venv
```

### 2. Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment
```bash
cp .env.example .env
```

### 5. Create Data Directory
```bash
mkdir -p data
```

### 6. Start the Agent
```bash
uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Testing the Agent

Once the server is running (you should see "Uvicorn running on http://0.0.0.0:8000"), open in your browser:

1. **Health Check:**
   http://localhost:8000/health

2. **Run Scan:**
   http://localhost:8000/scan

3. **Get Latest Signals:**
   http://localhost:8000/signals

4. **API Documentation:**
   http://localhost:8000/docs

5. **Alternative API Docs:**
   http://localhost:8000/redoc

---

## Testing via Command Line

In a new terminal (keep the server running):

```bash
# Health check
curl http://localhost:8000/health

# Run scan and get top 10 tokens
curl http://localhost:8000/scan

# Get top 5 tokens
curl http://localhost:8000/top?limit=5

# Get agent status
curl http://localhost:8000/status

# Get scan history
curl http://localhost:8000/history?limit=20
```

---

## Running via CLI (Single Scan)

In a new terminal:

```bash
source .venv/bin/activate  # or activate.bat on Windows
python -m crypto_agent.cli scan --limit 10
```

---

## Configuration

Edit `.env` to add your API keys:

```bash
nano .env  # or use any editor
```

### Recommended Free APIs:

- **Ethereum RPC:** Sign up at https://infura.io (free tier available)
- **Solana RPC:** Free public endpoint (already in .env.example)
- **Helius:** https://helius.xyz (free tier for Solana data)
- **OpenAI:** https://platform.openai.com (optional, for AI explanations)
- **Telegram Bot:** Create with @BotFather on Telegram (optional)
- **Discord Webhook:** Create in server settings (optional)

### Example .env Configuration:

```env
# AI Reasoning (optional)
OPENAI_API_KEY=sk-...

# Ethereum
ETHERSCAN_API_KEY=YourEtherscanKey
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY

# Solana
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=YOUR_HELIUS_KEY

# Alerts (optional)
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK
```

---

## Docker Installation

```bash
docker-compose up --build
```

Then open: http://localhost:8000

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'crypto_agent'"
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
uvicorn crypto_agent.main:app --port 8001  # Use different port
```

### "Python command not found"
Use `python3` instead of `python` on macOS/Linux

### Virtual environment won't activate
Try:
```bash
python3 -m venv .venv --clear
source .venv/bin/activate
```

---

## API Examples

### Get Top 10 Pump Candidates
```bash
curl -X GET "http://localhost:8000/scan?limit=10" \
  -H "accept: application/json"
```

### Get Top 5 High-Score Tokens
```bash
curl -X GET "http://localhost:8000/top?limit=5" \
  -H "accept: application/json"
```

### Response Example
```json
[
  {
    "token": "SOL",
    "symbol": "SOL",
    "chain": "solana",
    "score": 82.5,
    "probability": 0.75,
    "risk_level": "low",
    "reasons": [
      "Net inflow of $34,000,000 over the last hour",
      "Whale buying volume of $15,000,000",
      "290 large transfers indicate active participation"
    ],
    "metadata": {
      "market_cap_usd": 76000000000,
      "volume_24h_usd": 5200000000,
      "liquidity_usd": 2100000000,
      "inflow_usd_1h": 34000000,
      "whale_buy_volume_usd_1h": 15000000,
      "unique_buyers_1h": 980
    }
  }
]
```

---

## Stopping the Agent

Press `Ctrl+C` in the terminal where the server is running.

---

## Next Steps

1. **Test without API Keys:** The agent works in demo mode without keys
2. **Add Real Data:** Configure .env with your API keys to use live chain data
3. **Setup Alerts:** Add Telegram or Discord to get notified of high-score signals
4. **Backtest:** Run historical analysis to tune the scoring weights
5. **Deploy:** Use Docker or cloud hosting to run 24/7

---

## Support

For issues or questions:
- Check http://localhost:8000/docs for API documentation
- Review QUICKSTART.md for more details
- Check logs in the terminal for error messages

