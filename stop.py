#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stop web interface server.
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PID_FILE = ROOT / "web_server.pid"

def stop_server():
    """Stop web server."""
    if not PID_FILE.exists():
        print("Server is not running (PID file not found)")
        return
    
    try:
        pid = int(PID_FILE.read_text().strip())
    except (ValueError, FileNotFoundError):
        print("Invalid PID file")
        PID_FILE.unlink(missing_ok=True)
        return
    
    if sys.platform == "win32":
        # Windows: Use taskkill
        try:
            result = subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"Server stopped (PID: {pid})")
            else:
                # Try to find process by port instead
                print(f"Could not stop process {pid}, trying to find by port...")
                try:
                    import psutil
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            connections = proc.connections()
                            for conn in connections:
                                if conn.laddr.port == 5000:
                                    proc.terminate()
                                    proc.wait(timeout=5)
                                    print(f"Server stopped (found by port, PID: {proc.pid})")
                                    return
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            continue
                    print("Server process not found")
                except ImportError:
                    print(f"Failed to stop server (PID: {pid})")
                    print("Install psutil for better process management: pip install psutil")
        except FileNotFoundError:
            # Fallback: try using psutil if available
            try:
                import psutil
                process = psutil.Process(pid)
                process.terminate()
                process.wait(timeout=5)
                print(f"Server stopped (PID: {pid})")
            except (ImportError, psutil.NoSuchProcess, psutil.TimeoutExpired):
                print(f"Server process not found (PID: {pid})")
                print("Server may have already stopped")
    else:
        # Unix-like: Use kill
        try:
            subprocess.run(
                ["kill", "-TERM", str(pid)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"Server stopped (PID: {pid})")
        except subprocess.CalledProcessError:
            print(f"Failed to stop server (PID: {pid})")
            print("Server may have already stopped")
    
    # Remove PID file
    PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    stop_server()

