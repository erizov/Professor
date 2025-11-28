#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run enhancement script with progress reporting every 5 minutes.
"""

import subprocess
import threading
import time
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from queue import Queue

ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / "logs" / "enhancement_progress.log"
LOG_FILE.parent.mkdir(exist_ok=True)


def parse_output_line(line: str) -> Dict:
    """Parse output line for progress information."""
    result = {"type": "unknown", "line": line}
    
    # Enhanced line: [123/693] ✓ Enhanced: algorithm_name (Section1, Section2)
    enhanced_match = re.search(
        r"\[(\d+)/(\d+)\].*✓ Enhanced: (\w+).*\(([^)]+)\)", line
    )
    if enhanced_match:
        result = {
            "type": "enhanced",
            "current": int(enhanced_match.group(1)),
            "total": int(enhanced_match.group(2)),
            "algorithm": enhanced_match.group(3),
            "sections": [
                s.strip() for s in enhanced_match.group(4).split(",")
            ],
        }
    
    # Progress line: [PROGRESS] Enhanced 50/100 README files (50%)
    progress_match = re.search(
        r"\[PROGRESS\].*Enhanced (\d+)/(\d+).*\((\d+)%\)", line
    )
    if progress_match:
        result = {
            "type": "progress",
            "enhanced": int(progress_match.group(1)),
            "processed": int(progress_match.group(2)),
            "percentage": int(progress_match.group(3)),
        }
    
    # Complete line: [COMPLETE] Enhanced 350/693 README files
    complete_match = re.search(
        r"\[COMPLETE\].*Enhanced (\d+)/(\d+)", line
    )
    if complete_match:
        result = {
            "type": "complete",
            "enhanced": int(complete_match.group(1)),
            "total": int(complete_match.group(2)),
        }
    
    return result


class ProgressMonitor:
    """Monitor enhancement progress and report every 5 minutes."""
    
    def __init__(self):
        self.stats = {
            "start_time": datetime.now(),
            "last_report_time": datetime.now(),
            "total_enhanced": 0,
            "total_processed": 0,
            "percentage": 0,
            "section_counts": {},
            "recent_enhancements": [],
            "complete": False,
            "last_line": None,
        }
        self.output_queue = Queue()
        self.report_interval = timedelta(minutes=5)
    
    def update_stats(self, parsed: Dict):
        """Update statistics from parsed line."""
        if parsed["type"] == "enhanced":
            self.stats["total_enhanced"] += 1
            self.stats["total_processed"] = parsed["current"]
            
            # Track recent enhancements
            self.stats["recent_enhancements"].append(parsed)
            if len(self.stats["recent_enhancements"]) > 10:
                self.stats["recent_enhancements"].pop(0)
            
            # Count sections
            for section in parsed["sections"]:
                self.stats["section_counts"][section] = (
                    self.stats["section_counts"].get(section, 0) + 1
                )
        
        elif parsed["type"] == "progress":
            self.stats["total_enhanced"] = parsed["enhanced"]
            self.stats["total_processed"] = parsed["processed"]
            self.stats["percentage"] = parsed["percentage"]
        
        elif parsed["type"] == "complete":
            self.stats["complete"] = True
            self.stats["total_enhanced"] = parsed["enhanced"]
            self.stats["total_processed"] = parsed["total"]
            self.stats["percentage"] = (
                parsed["enhanced"] * 100 // parsed["total"]
                if parsed["total"] > 0
                else 0
            )
    
    def format_report(self) -> str:
        """Format progress report."""
        elapsed = datetime.now() - self.stats["start_time"]
        report = []
        report.append("=" * 70)
        report.append(
            f"Enhancement Progress Report - "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report.append("=" * 70)
        report.append("")
        
        if self.stats["complete"]:
            report.append("✅ PROCESS COMPLETE")
            report.append("")
            report.append(
                f"Total Enhanced: {self.stats['total_enhanced']}/"
                f"{self.stats['total_processed']}"
            )
            report.append(f"Success Rate: {self.stats['percentage']}%")
        else:
            report.append("📊 CURRENT STATUS")
            report.append("")
            if self.stats["total_processed"] > 0:
                report.append(
                    f"Processed: {self.stats['total_processed']} files "
                    f"({self.stats['percentage']}% success rate)"
                )
                report.append(
                    f"Enhanced: {self.stats['total_enhanced']} files"
                )
                
                # Estimate remaining
                if self.stats["total_processed"] > 0 and elapsed.total_seconds() > 0:
                    rate = self.stats["total_processed"] / elapsed.total_seconds()
                    # Estimate total files (assuming ~693 based on previous runs)
                    estimated_total = 693
                    remaining = estimated_total - self.stats["total_processed"]
                    if rate > 0 and remaining > 0:
                        remaining_seconds = remaining / rate
                        remaining_time = timedelta(seconds=int(remaining_seconds))
                        report.append(f"⏳ Estimated Remaining: {remaining_time}")
            else:
                report.append("Status: Starting up...")
            
            report.append("")
            report.append(f"⏱️  Elapsed Time: {elapsed}")
        
        report.append("")
        
        # Section statistics
        if self.stats["section_counts"]:
            report.append("📈 Section Enhancement Statistics:")
            for section, count in sorted(
                self.stats["section_counts"].items(), key=lambda x: -x[1]
            )[:5]:
                report.append(f"   - {section}: {count} files")
            report.append("")
        
        # Recent enhancements
        if self.stats["recent_enhancements"]:
            report.append("🔄 Recent Enhancements (last 5):")
            for enh in self.stats["recent_enhancements"][-5:]:
                sections = ", ".join(enh["sections"])
                report.append(
                    f"   - {enh['algorithm']} ({sections}) "
                    f"[{enh['current']}/{enh.get('total', '?')}]"
                )
            report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def should_report(self) -> bool:
        """Check if it's time for a progress report."""
        now = datetime.now()
        if now - self.stats["last_report_time"] >= self.report_interval:
            self.stats["last_report_time"] = now
            return True
        return False
    
    def print_report(self):
        """Print and save progress report."""
        report = self.format_report()
        print("\n" + report + "\n")
        
        # Save to file
        report_file = LOG_FILE.parent / "enhancement_reports.log"
        with open(report_file, "a", encoding="utf-8") as f:
            f.write(report + "\n\n")


def run_enhancement_with_monitoring():
    """Run enhancement script and monitor progress."""
    print("Starting enhancement process with progress monitoring...")
    print("Progress reports will be generated every 5 minutes.\n")
    
    monitor = ProgressMonitor()
    
    # Start enhancement process
    script_path = ROOT / "scripts" / "enhance_readmes_improved.py"
    process = subprocess.Popen(
        ["python", str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )
    
    # Monitor output
    try:
        for line in process.stdout:
            # Write to log file
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line)
            
            # Parse and update stats
            parsed = parse_output_line(line)
            monitor.update_stats(parsed)
            
            # Print line (for real-time feedback)
            print(line.rstrip())
            
            # Check if time for report
            if monitor.should_report():
                monitor.print_report()
        
        # Wait for process to complete
        process.wait()
        
        # Final report
        monitor.print_report()
        
        print(f"\nProcess completed with exit code: {process.returncode}")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Terminating...")
        process.terminate()
        process.wait()
        monitor.print_report()
    
    except Exception as e:
        print(f"\nError: {e}")
        process.terminate()
        monitor.print_report()


if __name__ == "__main__":
    run_enhancement_with_monitoring()


