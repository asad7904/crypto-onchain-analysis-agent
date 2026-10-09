#!/usr/bin/env python3
"""
Crypto On-chain Analysis Agent - Standalone Executable
Run this file directly with: python agent.py
No terminal commands needed.
"""

import sys
import os
import subprocess
import venv
from pathlib import Path

def ensure_python():
    """Verify Python 3.11+ is available."""
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_venv():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return venv_path
    
    print("Creating virtual environment...")
    venv.create(".venv", with_pip=True)
    print("✓ Virtual environment created")
    return venv_path

def get_pip_executable():
    """Get the pip executable path for the virtual environment."""
    venv_path = Path(".venv")
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"

def get_python_executable():
    """Get the Python executable path for the virtual environment."""
    venv_path = Path(".venv")
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"

def install_dependencies():
    """Install required packages."""
    print("Installing dependencies...")
    pip_exe = str(get_pip_executable())
    
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
    
    for package in packages:
        print(f"  Installing {package.split('>')[0]}...")
        subprocess.check_call([pip_exe, "install", "-q", package])
    
    print("✓ Dependencies installed")

def setup_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file already exists")
        return
    
    env_example = Path(".env.example")
    if env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✓ .env file created from template")
    else:
        env_file.write_text(
            """OPENAI_API_KEY=
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
        )
        print("✓ .env file created with defaults")

def create_data_dir():
    """Create data directory."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✓ Data directory ready")

def run_agent():
    """Start the agent."""
    print("\n" + "="*50)
    print("🚀 Starting Crypto On-chain Analysis Agent")
    print("="*50)
    print("\n")
    print("✓ API Server: http://localhost:8000")
    print("✓ Docs: http://localhost:8000/docs")
    print("✓ Health: http://localhost:8000/health")
    print("✓ Scan: http://localhost:8000/scan")
    print("\nPress Ctrl+C to stop\n")
    
    python_exe = str(get_python_executable())
    subprocess.call([python_exe, "-m", "uvicorn", "crypto_agent.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

def main():
    """Main installation and startup sequence."""
    print("\n" + "="*60)
    print("Crypto On-chain Analysis Agent - Auto Installer & Runner")
    print("="*60 + "\n")
    
    try:
        ensure_python()
        create_venv()
        install_dependencies()
        setup_env_file()
        create_data_dir()
        
        print("\n" + "="*60)
        print("✅ Installation Complete!")
        print("="*60 + "\n")
        
        run_agent()
    except KeyboardInterrupt:
        print("\n\nShutdown requested by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
