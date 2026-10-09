@echo off
REM Crypto On-chain Analysis Agent - Windows Auto Setup & Run
REM This script does everything automatically

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Crypto Agent - Auto Setup (Windows)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed!
    echo Please install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [PASS] %PYTHON_VERSION%

echo.
echo [1/5] Creating virtual environment...
if exist ".venv" (
    echo [SKIP] Virtual environment already exists
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo X Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [PASS] Virtual environment created
)

echo.
echo [2/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo X Failed to activate virtual environment
    pause
    exit /b 1
)
echo [PASS] Virtual environment activated

echo.
echo [3/5] Installing dependencies...
pip install -q fastapi uvicorn httpx pydantic pydantic-settings python-dotenv apscheduler numpy pandas openai
if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)
echo [PASS] Dependencies installed

echo.
echo [4/5] Setting up environment file...
if exist ".env" (
    echo [SKIP] .env file already exists
) else (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [PASS] .env file created from template
    ) else (
        (
            echo OPENAI_API_KEY=
            echo ETHERSCAN_API_KEY=
            echo ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
            echo SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
            echo HELIUS_API_KEY=
            echo COINGECKO_API_URL=https://api.coingecko.com/api/v3
            echo LOG_LEVEL=INFO
            echo APP_ENV=development
            echo TELEGRAM_BOT_TOKEN=
            echo TELEGRAM_CHAT_ID=
            echo DISCORD_WEBHOOK_URL=
        ) > .env
        echo [PASS] .env file created with defaults
    )
)

echo.
echo [5/5] Creating data directory...
if not exist "data" mkdir data
echo [PASS] Data directory ready

echo.
echo ========================================
echo [SUCCESS] Installation Complete!
echo ========================================
echo.
echo. 
echo Starting Crypto On-chain Analysis Agent...
echo.
echo [INFO] API Server: http://localhost:8000
echo [INFO] Swagger Docs: http://localhost:8000/docs
echo [INFO] ReDoc: http://localhost:8000/redoc
echo [INFO] Health Check: http://localhost:8000/health
echo [INFO] Run Scan: http://localhost:8000/scan
echo.
echo Press Ctrl+C to stop
echo.

REM Start the agent
python -m uvicorn crypto_agent.main:app --reload --host 0.0.0.0 --port 8000

if errorlevel 1 (
    echo.
    echo X Failed to start agent
    echo Check that all dependencies are installed
    pause
    exit /b 1
)

pause
