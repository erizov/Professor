#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spaced repetition tracker for algorithm learning.
Tracks review schedules and generates daily review prompts.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
TRACKER_FILE = ROOT / "spaced_repetition_tracker.json"

# Review intervals (days)
REVIEW_INTERVALS = [1, 3, 7, 14, 30, 90, 180]

class SpacedRepetitionTracker:
    """Track spaced repetition for algorithms."""
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load tracker data from file."""
        if TRACKER_FILE.exists():
            with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "algorithms": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_data(self):
        """Save tracker data to file."""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
    
    def learn_algorithm(self, algorithm_name: str, date: Optional[datetime] = None):
        """Mark algorithm as learned."""
        if date is None:
            date = datetime.now()
        
        self.data["algorithms"][algorithm_name] = {
            "learned_date": date.isoformat(),
            "reviews": [],
            "next_review": (date + timedelta(days=REVIEW_INTERVALS[0])).isoformat(),
            "review_level": 0,
            "mastery_level": 0
        }
        self._save_data()
        print(f"✓ Learned: {algorithm_name}")
        print(f"  Next review: {self.data['algorithms'][algorithm_name]['next_review']}")
    
    def complete_review(self, algorithm_name: str, performance: str = "good"):
        """Mark review as completed."""
        if algorithm_name not in self.data["algorithms"]:
            print(f"Error: {algorithm_name} not found. Learn it first.")
            return
        
        algo = self.data["algorithms"][algorithm_name]
        review_date = datetime.now()
        
        # Record review
        algo["reviews"].append({
            "date": review_date.isoformat(),
            "performance": performance,
            "review_level": algo["review_level"]
        })
        
        # Update mastery level
        if performance == "excellent":
            algo["mastery_level"] = min(100, algo["mastery_level"] + 15)
        elif performance == "good":
            algo["mastery_level"] = min(100, algo["mastery_level"] + 10)
        elif performance == "fair":
            algo["mastery_level"] = min(100, algo["mastery_level"] + 5)
        
        # Move to next review level
        algo["review_level"] += 1
        
        # Calculate next review date
        if algo["review_level"] < len(REVIEW_INTERVALS):
            days = REVIEW_INTERVALS[algo["review_level"]]
        else:
            days = 30  # Monthly maintenance
        
        algo["next_review"] = (review_date + timedelta(days=days)).isoformat()
        
        self._save_data()
        print(f"✓ Review completed: {algorithm_name}")
        print(f"  Review level: {algo['review_level']}/{len(REVIEW_INTERVALS)}")
        print(f"  Mastery: {algo['mastery_level']}%")
        print(f"  Next review: {algo['next_review']}")
    
    def get_due_reviews(self, date: Optional[datetime] = None) -> List[Dict]:
        """Get algorithms due for review."""
        if date is None:
            date = datetime.now()
        
        due = []
        for name, algo in self.data["algorithms"].items():
            next_review = datetime.fromisoformat(algo["next_review"])
            if next_review <= date:
                due.append({
                    "name": name,
                    "review_level": algo["review_level"],
                    "mastery_level": algo["mastery_level"],
                    "days_overdue": (date - next_review).days
                })
        
        return sorted(due, key=lambda x: x["days_overdue"], reverse=True)
    
    def get_daily_review_plan(self, max_time: int = 60) -> Dict:
        """Generate daily review plan."""
        due = self.get_due_reviews()
        
        # Estimate time per review (minutes)
        time_estimates = {
            0: 10,  # First review
            1: 15,  # Second review
            2: 20,  # Third review
            3: 25,  # Fourth review
            4: 30,  # Fifth review
        }
        
        plan = []
        total_time = 0
        
        for algo in due:
            level = algo["review_level"]
            time_needed = time_estimates.get(level, 30)
            
            if total_time + time_needed <= max_time:
                plan.append({
                    "algorithm": algo["name"],
                    "review_level": level,
                    "estimated_time": time_needed,
                    "mastery_level": algo["mastery_level"]
                })
                total_time += time_needed
            else:
                break
        
        return {
            "date": datetime.now().isoformat(),
            "algorithms": plan,
            "total_time": total_time,
            "remaining_due": len(due) - len(plan)
        }
    
    def print_daily_plan(self):
        """Print daily review plan."""
        plan = self.get_daily_review_plan()
        
        print("=" * 70)
        print("DAILY REVIEW PLAN")
        print("=" * 70)
        print(f"Date: {plan['date']}")
        print(f"Total Time: {plan['total_time']} minutes")
        print()
        
        if not plan["algorithms"]:
            print("No reviews due today! 🎉")
            return
        
        for i, algo in enumerate(plan["algorithms"], 1):
            print(f"{i}. {algo['algorithm']}")
            print(f"   Review Level: {algo['review_level'] + 1}")
            print(f"   Mastery: {algo['mastery_level']}%")
            print(f"   Time: {algo['estimated_time']} minutes")
            print()
        
        if plan["remaining_due"] > 0:
            print(f"Note: {plan['remaining_due']} more algorithms due for review")
            print("Consider extending your study time or prioritizing.")
    
    def get_statistics(self) -> Dict:
        """Get learning statistics."""
        algorithms = self.data["algorithms"]
        
        total = len(algorithms)
        mastered = sum(1 for a in algorithms.values() if a["mastery_level"] >= 80)
        in_progress = sum(1 for a in algorithms.values() if 0 < a["mastery_level"] < 80)
        due_reviews = len(self.get_due_reviews())
        
        return {
            "total_algorithms": total,
            "mastered": mastered,
            "in_progress": in_progress,
            "due_reviews": due_reviews,
            "average_mastery": sum(a["mastery_level"] for a in algorithms.values()) / total if total > 0 else 0
        }

def main():
    """CLI interface for spaced repetition tracker."""
    import sys
    
    tracker = SpacedRepetitionTracker()
    
    if len(sys.argv) < 2:
        tracker.print_daily_plan()
        return
    
    command = sys.argv[1].lower()
    
    if command == "learn" and len(sys.argv) > 2:
        algorithm = " ".join(sys.argv[2:])
        tracker.learn_algorithm(algorithm)
    
    elif command == "review" and len(sys.argv) > 2:
        algorithm = " ".join(sys.argv[2:])
        performance = sys.argv[3] if len(sys.argv) > 3 else "good"
        tracker.complete_review(algorithm, performance)
    
    elif command == "due":
        due = tracker.get_due_reviews()
        print(f"Algorithms due for review: {len(due)}")
        for algo in due:
            print(f"  - {algo['name']} (Level {algo['review_level'] + 1}, {algo['days_overdue']} days overdue)")
    
    elif command == "stats":
        stats = tracker.get_statistics()
        print("Learning Statistics:")
        print(f"  Total Algorithms: {stats['total_algorithms']}")
        print(f"  Mastered (80%+): {stats['mastered']}")
        print(f"  In Progress: {stats['in_progress']}")
        print(f"  Due Reviews: {stats['due_reviews']}")
        print(f"  Average Mastery: {stats['average_mastery']:.1f}%")
    
    elif command == "plan":
        tracker.print_daily_plan()
    
    else:
        print("Usage:")
        print("  python spaced_repetition_tracker.py                    # Show daily plan")
        print("  python spaced_repetition_tracker.py learn <algorithm>  # Mark as learned")
        print("  python spaced_repetition_tracker.py review <algorithm> [performance]  # Complete review")
        print("  python spaced_repetition_tracker.py due                # Show due reviews")
        print("  python spaced_repetition_tracker.py stats              # Show statistics")
        print("  python spaced_repetition_tracker.py plan               # Show daily plan")

if __name__ == "__main__":
    main()

