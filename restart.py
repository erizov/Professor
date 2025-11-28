#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restart web interface server.
Combines stop and start functionality.
"""

import sys
import time
from pathlib import Path

# Import stop and start functions
from stop import stop_server
from start import start_server

def restart_server():
    """Stop the server if running, then start it again."""
    print("=" * 60)
    print("RESTARTING WEB SERVER")
    print("=" * 60)
    
    # Step 1: Stop the server
    print("\n[1/2] Stopping server...")
    stop_server()
    
    # Wait a moment for the server to fully stop
    print("\nWaiting for server to fully stop...")
    time.sleep(2)
    
    # Step 2: Start the server
    print("\n[2/2] Starting server...")
    start_server()
    
    print("\n" + "=" * 60)
    print("RESTART COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    restart_server()

