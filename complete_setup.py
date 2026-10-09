#!/usr/bin/env python3
"""
Complete setup in pure Python - works on all platforms
Just run: python complete_setup.py
"""

import os
import sys
import subprocess
import venv
from pathlib import Path
import shutil

# ANSI color codes for pretty output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'
BOLD = '\033[1m'

def print_step(msg):
    print(f"{BLUE}{msg}{END}")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{END}")

def print_error(msg):
    print(f"{RED}✗ {msg}{END}")

def print_info(msg):
    print(f"{YELLOW}ℹ {msg}{END}")

def get_venv_paths():
    """Get Python and pip paths for virtual environment."""
    venv_path = Path(".venv")
    if sys.platform == "win32":
        return str(venv_path / "Scripts" / "python.exe"), str(venv_path / "Scripts" / "pip.exe")
    return str(venv_path / "bin" / "python"), str(venv_path / "bin" / "pip")

def step1_create_venv():
    """Step 1: Create virtual environment."""
    print_step("\n[1/5] Creating virtual environment...")
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print_info("Virtual environment already exists")
        return
    
    try:
        venv.create(".venv", with_pip=True)
        print_success("Virtual environment created")
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        sys.exit(1)

def step2_install_dependencies():
    """Step 2: Install required packages."""
    print_step("\n[2/5] Installing dependencies...")
    
    _, pip_exe = get_venv_paths()
    
    packages = [
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.29.0",
        "httpx>=0.27.0",
        "pydantic>=2.7.0",
        "pydantic-settings>=2.3.0",
        "python-dotenv>=1.0.1",
        "apscheduler>=3.10.4",
        "numpy>=1.26.0",
        "pandas>=2.2.0",
        "openai>=1.30.0",
    ]
    
    try:
        for package in packages:
            pkg_name = package.split('>')[0].split('<')[0].split('=')[0]
            print(f"  Installing {pkg_name}...", end=" ", flush=True)
            subprocess.check_call(
                [pip_exe, "install", "-q", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"{GREEN}✓{END}")
        
        print_success("Dependencies installed")
    except Exception as e:
        print_error(f"Failed to install dependencies: {e}")
        sys.exit(1)

def step3_setup_env():
    """Step 3: Create .env file."""
    print_step("\n[3/5] Setting up environment file...")
    
    env_file = Path(".env")
    if env_file.exists():
        print_info(".env file already exists")
        return
    
    env_content = """OPENAI_API_KEY=
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
"""
    
    try:
        env_file.write_text(env_content)
        print_success(".env file created")
    except Exception as e:
        print_error(f"Failed to create .env: {e}")
        sys.exit(1)

def step4_create_data_dir():
    """Step 4: Create data directory."""
    print_step("\n[4/5] Creating data directory...")
    
    try:
        Path("data").mkdir(exist_ok=True)
        print_success("Data directory created")
    except Exception as e:
        print_error(f"Failed to create data directory: {e}")
        sys.exit(1)

def step5_start_agent():
    """Step 5: Start the agent."""
    print_step("\n[5/5] Starting the Agent...")
    
    python_exe, _ = get_venv_paths()
    
    print(f"""
{BOLD}{'='*60}{END}
{BOLD}{GREEN}✅ Installation Complete!{END}{BOLD}{END}
{BOLD}{'='*60}{END}

{BOLD}🚀 Crypto On-chain Analysis Agent Starting...{END}

{BOLD}📍 API Endpoints:{END}
  • Health Check:  {BLUE}http://localhost:8000/health{END}
  • Run Scan:      {BLUE}http://localhost:8000/scan{END}
  • Get Signals:   {BLUE}http://localhost:8000/signals{END}
  • API Docs:      {BLUE}http://localhost:8000/docs{END}
  • ReDoc:         {BLUE}http://localhost:8000/redoc{END}

{BOLD}📊 Status Endpoint:{END}
  • Status:        {BLUE}http://localhost:8000/status{END}
  • History:       {BLUE}http://localhost:8000/history{END}

{BOLD}🛑 To stop: Press Ctrl+C{END}

{BOLD}{'='*60}{END}
""")
    
    try:
        subprocess.call([python_exe, "-m", "uvicorn", "crypto_agent.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Shutdown requested by user{END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Failed to start agent: {e}")
        sys.exit(1)

def main():
    """Run all setup steps."""
    print(f"""
{BOLD}{BLUE}{'='*60}{END}
{BOLD}{BLUE}Crypto On-chain Analysis Agent{END}
{BOLD}{BLUE}Complete Automated Setup{END}
{BOLD}{BLUE}{'='*60}{END}
""")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    
    python_version = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print_success(python_version)
    
    try:
        step1_create_venv()
        step2_install_dependencies()
        step3_setup_env()
        step4_create_data_dir()
        step5_start_agent()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Setup cancelled by user{END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
