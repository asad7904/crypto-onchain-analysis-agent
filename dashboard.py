#!/usr/bin/env python3
"""
Web Dashboard for Crypto On-chain Analysis Agent
Access at http://localhost:8000 after running this script
"""

import sys
import subprocess
from pathlib import Path

def get_python_executable():
    """Get the Python executable path for the virtual environment."""
    venv_path = Path(".venv")
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"

def main():
    print("\n" + "="*60)
    print("Starting Crypto Agent Web Dashboard")
    print("="*60 + "\n")
    
    print("✓ API Server: http://localhost:8000")
    print("✓ Swagger Docs: http://localhost:8000/docs")
    print("✓ ReDoc: http://localhost:8000/redoc")
    print("\nOpening browser in 2 seconds...\n")
    
    import time
    time.sleep(2)
    
    # Try to open browser
    try:
        import webbrowser
        webbrowser.open("http://localhost:8000")
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please open http://localhost:8000 in your browser manually.")
    
    python_exe = str(get_python_executable())
    subprocess.call([python_exe, "-m", "uvicorn", "crypto_agent.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown requested.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
