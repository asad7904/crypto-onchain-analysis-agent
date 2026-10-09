#!/usr/bin/env python3
"""
One-time setup + agent runner
Run this script once, then use dashboard.py or run_agent.py
"""

import subprocess
import sys

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Crypto Agent - Setup & Run")
    print("="*60 + "\n")
    
    try:
        print("Step 1: Installing and setting up...")
        subprocess.check_call([sys.executable, "agent.py"])
    except KeyboardInterrupt:
        print("\n\nShutdown requested.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
