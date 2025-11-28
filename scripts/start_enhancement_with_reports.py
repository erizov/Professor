#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Start enhancement process and report progress every 5 minutes.
"""

import subprocess
import threading
import time
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / "logs" / "enhancement_progress.log"
LOG_FILE.parent.mkdir(exist_ok=True)


class ProgressReporter:
    """Report progress every 5 minutes."""
    
    def __init__(self):
        self.stats = {
            "start_time": datetime.now(),
            "total_enhanced": 0,
            "total_processed": 0,
            "section_counts": {},
            "recent_enhancements": [],
            "complete": False,
        }
        self.last_report = datetime.now()
        self.report_interval = timedelta(minutes=5)
    
    def parse_line(self, line: str):
        """Parse output line and update stats."""
        # Enhanced: [123/693] ✓ Enhanced: algorithm (Section1, Section2)
        match = re.search(
            r"\[(\d+)/(\d+)\].*✓ Enhanced: (\w+).*\(([^)]+)\)", line
        )
        if match:
            self.stats["total_enhanced"] += 1
            self.stats["total_processed"] = int(match.group(1))
            algorithm = match.group(3)
            sections = [s.strip() for s in match.group(4).split(",")]
            
            self.stats["recent_enhancements"].append({
                "algorithm": algorithm,
                "sections": sections,
                "index": int(match.group(1)),
            })
            if len(self.stats["recent_enhancements"]) > 10:
                self.stats["recent_enhancements"].pop(0)
            
            for section in sections:
                self.stats["section_counts"][section] = (
                    self.stats["section_counts"].get(section, 0) + 1
                )
            return
        
        # Progress: [PROGRESS] Enhanced 50/100 (50%)
        match = re.search(
            r"\[PROGRESS\].*Enhanced (\d+)/(\d+).*\((\d+)%\)", line
        )
        if match:
            self.stats["total_enhanced"] = int(match.group(1))
            self.stats["total_processed"] = int(match.group(2))
            return
        
        # Complete: [COMPLETE] Enhanced 350/693
        match = re.search(r"\[COMPLETE\].*Enhanced (\d+)/(\d+)", line)
        if match:
            self.stats["complete"] = True
            self.stats["total_enhanced"] = int(match.group(1))
            self.stats["total_processed"] = int(match.group(2))
    
    def should_report(self) -> bool:
        """Check if it's time for a report."""
        now = datetime.now()
        if now - self.last_report >= self.report_interval:
            self.last_report = now
            return True
        return False
    
    def print_report(self):
        """Print progress report."""
        elapsed = datetime.now() - self.stats["start_time"]
        
        print("\n" + "=" * 70)
        print(
            f"📊 PROGRESS REPORT - "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print("=" * 70)
        
        if self.stats["complete"]:
            print("✅ PROCESS COMPLETE!")
            print(
                f"Total Enhanced: {self.stats['total_enhanced']}/"
                f"{self.stats['total_processed']}"
            )
            if self.stats["total_processed"] > 0:
                percentage = (
                    self.stats["total_enhanced"] * 100
                    // self.stats["total_processed"]
                )
                print(f"Success Rate: {percentage}%")
        else:
            print(f"⏱️  Elapsed Time: {elapsed}")
            print(f"📁 Processed: {self.stats['total_processed']} files")
            print(f"✅ Enhanced: {self.stats['total_enhanced']} files")
            
            if self.stats["total_processed"] > 0:
                percentage = (
                    self.stats["total_enhanced"] * 100
                    // self.stats["total_processed"]
                )
                print(f"📈 Success Rate: {percentage}%")
                
                # Estimate remaining
                if elapsed.total_seconds() > 0:
                    rate = self.stats["total_processed"] / elapsed.total_seconds()
                    estimated_total = 693
                    remaining = estimated_total - self.stats["total_processed"]
                    if rate > 0 and remaining > 0:
                        remaining_sec = remaining / rate
                        remaining_time = timedelta(seconds=int(remaining_sec))
                        print(f"⏳ Estimated Remaining: {remaining_time}")
        
        if self.stats["section_counts"]:
            print("\n📈 Top Enhanced Sections:")
            for section, count in sorted(
                self.stats["section_counts"].items(), key=lambda x: -x[1]
            )[:5]:
                print(f"   - {section}: {count} files")
        
        if self.stats["recent_enhancements"]:
            print("\n🔄 Recent Enhancements (last 5):")
            for enh in self.stats["recent_enhancements"][-5:]:
                sections = ", ".join(enh["sections"])
                print(
                    f"   - {enh['algorithm']} ({sections}) "
                    f"[{enh['index']}]"
                )
        
        print("=" * 70 + "\n")


def run_with_progress_reporting():
    """Run enhancement and report progress every 5 minutes."""
    print("Starting enhancement process...")
    print("Progress reports will be generated every 5 minutes.\n")
    
    reporter = ProgressReporter()
    script_path = ROOT / "scripts" / "enhance_readmes_improved.py"
    
    # Start process
    process = subprocess.Popen(
        ["python", str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )
    
    try:
        # Read output line by line
        for line in iter(process.stdout.readline, ""):
            if not line:
                break
            
            # Write to log
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line)
            
            # Parse and update stats
            reporter.parse_line(line)
            
            # Print line (real-time output)
            print(line.rstrip())
            
            # Check if time for report
            if reporter.should_report():
                reporter.print_report()
        
        # Wait for completion
        process.wait()
        
        # Final report
        reporter.print_report()
        print(f"\n✅ Process completed with exit code: {process.returncode}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted. Terminating...")
        process.terminate()
        process.wait()
        reporter.print_report()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        process.terminate()
        reporter.print_report()


if __name__ == "__main__":
    run_with_progress_reporting()

