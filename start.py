#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start web interface server in background.
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PID_FILE = ROOT / "web_server.pid"

def start_server():
    """Start web server in background."""
    # Check if server is already running
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        try:
            # Check if process is still running (Windows)
            import psutil
            if psutil.pid_exists(pid):
                print(f"Server is already running (PID: {pid})")
                return
        except (ImportError, psutil.NoSuchProcess):
            # If psutil not available or process doesn't exist, continue
            pass
        except Exception:
            # If other error, continue
            pass
    
    # Start server in background
    script_path = ROOT / "scripts" / "run_web_interface.py"
    
    if sys.platform == "win32":
        # Windows: Use CREATE_NEW_PROCESS_GROUP and DETACHED_PROCESS
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(ROOT),
            stdin=subprocess.DEVNULL
        )
    else:
        # Unix-like: Use nohup or similar
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(ROOT),
            start_new_session=True,
            stdin=subprocess.DEVNULL
        )
    
    # Save PID
    PID_FILE.write_text(str(process.pid), encoding='utf-8')
    
    print(f"Web server started in background (PID: {process.pid})")
    print("Server URL: http://localhost:5000")
    print(f"Use 'python stop.py' to stop the server")


if __name__ == "__main__":
    start_server()

