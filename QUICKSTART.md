# Crypto On-chain Analysis Agent — Quick Start Guide

A production-ready AI agent that scans on-chain crypto data hourly across Solana, Ethereum, and other ecosystems to identify tokens most likely to pump based on inflow, whale activity, and liquidity health.

## Quick Start (3 Steps)

### Option 1: Automated Setup (Linux/Mac)

```bash
cd crypto-onchain-analysis-agent
bash setup.sh
bash run.sh
```

Then open: **http://localhost:8000/scan**

### Option 2: Manual Setup

#### Step 1: Install Dependencies

```bash
cd crypto-onchain-analysis-agent
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
mkdir -p data
```

#### Step 2: Run the Agent

**Start the API server:**
```bash
uvicorn crypto_agent.main:app --reload
```

The agent will start scanning hourly and expose an API on `http://localhost:8000`

**Or run a single scan via CLI:**
```bash
python -m crypto_agent.cli scan --limit 10
```

#### Step 3: Query the Agent

Open your browser or use curl:

```bash
# Health check
curl http://localhost:8000/health

# Run a scan and get top 10 tokens
curl http://localhost:8000/scan

# Get latest signals
curl http://localhost:8000/signals

# Get top N tokens
curl http://localhost:8000/top?limit=5

# Get agent status
curl http://localhost:8000/status
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/scan` | GET | Run scan, save results, return top tokens |
| `/signals` | GET | Get latest scan results |
| `/top?limit=N` | GET | Get top N tokens from latest scan |
| `/status` | GET | Agent status and scan history |

## Example Response

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
      "290 large transfers indicate active participation",
      "1h momentum is +2.80%"
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

## Configuration

Edit `.env` to add your API keys:

```env
# AI Reasoning (optional)
OPENAI_API_KEY=sk-...

# On-chain Data (optional - uses public APIs by default)
ETHERSCAN_API_KEY=
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=
COINGECKO_API_URL=https://api.coingecko.com/api/v3

# Alerts (optional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DISCORD_WEBHOOK_URL=
```

## How It Works

1. **Data Collection**: Scans Solana, Ethereum, and other chains every hour
2. **Normalization**: Converts chain-specific data to unified metrics
3. **Scoring**: Ranks tokens based on:
   - Net inflow (30%)
   - Whale buy pressure (25%)
   - Unique buyer growth (15%)
   - Large transaction activity (10%)
   - Liquidity health (10%)
   - 1h momentum (10%)
4. **Risk Adjustment**: Subtracts penalties for:
   - Sell pressure
   - Low liquidity
   - High concentration risk
5. **Ranking**: Returns top candidates by pump probability
6. **Alerts**: Sends Telegram/Discord notifications if configured

## Docker Support

```bash
docker-compose up --build
```

Then access: **http://localhost:8000**

## CLI Usage

```bash
# Run a single scan
python -m crypto_agent.cli scan

# Get top 5 tokens
python -m crypto_agent.cli top --limit 5

# Export runtime config
python -m crypto_agent.runtime_config
```

## File Structure

```
crypto-onchain-analysis-agent/
├── crypto_agent/
│   ├── main.py           # FastAPI app and scheduler
│   ├── service.py        # SignalAgent orchestrator
│   ├── collectors.py     # Multi-chain data collectors
│   ├── engine.py         # Scoring and ranking engine
│   ├── models.py         # Pydantic data models
│   ├── storage.py        # SQLite scan history
│   ├── alerts.py         # Telegram/Discord notifications
│   ├── config.py         # Settings and configuration
│   ├── cli.py            # Command-line interface
│   └── runtime_config.py # Config export
├── data/                 # SQLite database and scan history
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image
├── docker-compose.yml    # Multi-container setup
├── setup.sh              # Automated setup script
├── run.sh                # Run agent script
└── scan.sh               # Run single scan script
```

## What Gets Detected

The agent identifies coins most likely to pump when:

✓ Large net inflows in the last hour
✓ Whale accumulation and large buy orders
✓ Rising unique buyer count (wallet growth)
✓ High volume of large transfers
✓ Healthy liquidity (not a rugpull trap)
✓ Positive 1h momentum
✗ No excessive sell pressure
✗ Not overly concentrated in few wallets

## Performance Tuning

Scoring weights are in `crypto_agent/engine.py`. Adjust to your risk preference:

- Increase inflow_score weight → detect earlier
- Increase liquidity_score weight → avoid rugs
- Decrease risk_penalty → more aggressive

## Troubleshooting

### "ModuleNotFoundError: No module named 'crypto_agent'"

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### API not responding

Check if port 8000 is in use:
```bash
lsof -i :8000  # Kill with: kill -9 <PID>
```

### No data returned

The demo mode returns synthetic data. To use real chains, add API keys to `.env`.

## Next Steps

1. **Add API Keys**: Configure Etherscan, Helius, or OpenAI in `.env`
2. **Test Endpoints**: Query `/scan` and review results
3. **Set Alerts**: Add Telegram bot token and chat ID for notifications
4. **Deploy**: Use Docker or cloud hosting (AWS, GCP, Railway, Replit)
5. **Backtesting**: Compare ranked signals against actual 1h/4h returns to tune weights

## Support

For issues or questions, refer to the repository:
https://github.com/asad7904/crypto-onchain-analysis-agent

## License

MIT
