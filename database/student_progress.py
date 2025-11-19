#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Student progress tracking system.
Tracks algorithm completion, test scores, and learning progress.
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"


def create_progress_schema(cursor):
    """Create student progress tracking tables."""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS algorithm_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            algorithm_id INTEGER NOT NULL,
            status TEXT DEFAULT 'not_started',  -- not_started, in_progress, completed
            completion_date TIMESTAMP,
            time_spent_minutes INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            last_accessed TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id),
            UNIQUE(student_id, algorithm_id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            algorithm_id INTEGER NOT NULL,
            test_score REAL,
            total_tests INTEGER,
            passed_tests INTEGER,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS learning_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            path_name TEXT,
            algorithms_completed INTEGER DEFAULT 0,
            total_algorithms INTEGER,
            progress_percentage REAL DEFAULT 0.0,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            achievement_type TEXT,  -- first_complete, streak, perfect_score, etc.
            achievement_name TEXT,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """
    )

    # Indexes
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_progress_student ON algorithm_progress(student_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_progress_algorithm ON algorithm_progress(algorithm_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_tests_student ON test_results(student_id)"
    )


class StudentProgressTracker:
    """Track and manage student progress."""

    def __init__(self, student_id: str):
        """
        Initialize progress tracker for a student.

        Args:
            student_id: Unique student identifier
        """
        self.student_id = student_id
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        create_progress_schema(cursor)
        self.conn.commit()

        # Ensure student exists
        cursor.execute(
            """
            INSERT OR IGNORE INTO students (student_id) VALUES (?)
        """,
            (student_id,),
        )
        self.conn.commit()

    def start_algorithm(self, algorithm_id: int):
        """Mark algorithm as started."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO algorithm_progress
            (student_id, algorithm_id, status, last_accessed, attempts)
            VALUES (?, ?, 'in_progress', ?, 
                    COALESCE((SELECT attempts FROM algorithm_progress 
                             WHERE student_id = ? AND algorithm_id = ?), 0) + 1)
        """,
            (
                self.student_id,
                algorithm_id,
                datetime.now().isoformat(),
                self.student_id,
                algorithm_id,
            ),
        )
        self.conn.commit()

    def complete_algorithm(self, algorithm_id: int, time_spent_minutes: int = 0):
        """Mark algorithm as completed."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE algorithm_progress
            SET status = 'completed',
                completion_date = ?,
                time_spent_minutes = time_spent_minutes + ?,
                last_accessed = ?
            WHERE student_id = ? AND algorithm_id = ?
        """,
            (
                datetime.now().isoformat(),
                time_spent_minutes,
                datetime.now().isoformat(),
                self.student_id,
                algorithm_id,
            ),
        )
        self.conn.commit()

        # Check for achievements
        self._check_achievements()

    def record_test_result(
        self, algorithm_id: int, test_score: float, total_tests: int, passed_tests: int
    ):
        """Record test results."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO test_results
            (student_id, algorithm_id, test_score, total_tests, passed_tests)
            VALUES (?, ?, ?, ?, ?)
        """,
            (self.student_id, algorithm_id, test_score, total_tests, passed_tests),
        )
        self.conn.commit()

        # Update progress if perfect score
        if test_score == 100.0:
            self.complete_algorithm(algorithm_id)

    def get_progress_summary(self) -> Dict:
        """Get overall progress summary."""
        cursor = self.conn.cursor()

        # Total algorithms
        cursor.execute("SELECT COUNT(*) as total FROM algorithms")
        total = cursor.fetchone()["total"]

        # Completed algorithms
        cursor.execute(
            """
            SELECT COUNT(*) as completed
            FROM algorithm_progress
            WHERE student_id = ? AND status = 'completed'
        """,
            (self.student_id,),
        )
        completed = cursor.fetchone()["completed"]

        # In progress
        cursor.execute(
            """
            SELECT COUNT(*) as in_progress
            FROM algorithm_progress
            WHERE student_id = ? AND status = 'in_progress'
        """,
            (self.student_id,),
        )
        in_progress = cursor.fetchone()["in_progress"]

        # Average test score
        cursor.execute(
            """
            SELECT AVG(test_score) as avg_score
            FROM test_results
            WHERE student_id = ?
        """,
            (self.student_id,),
        )
        avg_score = cursor.fetchone()["avg_score"] or 0

        # Total time spent
        cursor.execute(
            """
            SELECT SUM(time_spent_minutes) as total_time
            FROM algorithm_progress
            WHERE student_id = ?
        """,
            (self.student_id,),
        )
        total_time = cursor.fetchone()["total_time"] or 0

        # Achievements
        cursor.execute(
            """
            SELECT COUNT(*) as achievement_count
            FROM achievements
            WHERE student_id = ?
        """,
            (self.student_id,),
        )
        achievements = cursor.fetchone()["achievement_count"]

        return {
            "total_algorithms": total,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": total - completed - in_progress,
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
            "average_test_score": round(avg_score, 2),
            "total_time_minutes": total_time,
            "total_time_hours": round(total_time / 60, 2),
            "achievements": achievements,
        }

    def get_algorithm_progress(self, algorithm_id: int) -> Optional[Dict]:
        """Get progress for specific algorithm."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM algorithm_progress
            WHERE student_id = ? AND algorithm_id = ?
        """,
            (self.student_id, algorithm_id),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Get recent activity."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT ap.*, a.name, a.display_name
            FROM algorithm_progress ap
            JOIN algorithms a ON ap.algorithm_id = a.id
            WHERE ap.student_id = ?
            ORDER BY ap.last_accessed DESC
            LIMIT ?
        """,
            (self.student_id, limit),
        )
        return [dict(row) for row in cursor.fetchall()]

    def _check_achievements(self):
        """Check and award achievements."""
        cursor = self.conn.cursor()

        # First completion
        cursor.execute(
            """
            SELECT COUNT(*) as count FROM algorithm_progress
            WHERE student_id = ? AND status = 'completed'
        """,
            (self.student_id,),
        )
        completed_count = cursor.fetchone()["count"]

        if completed_count == 1:
            cursor.execute(
                """
                INSERT OR IGNORE INTO achievements
                (student_id, achievement_type, achievement_name)
                VALUES (?, 'first_complete', 'First Algorithm Completed')
            """,
                (self.student_id,),
            )

        # Milestones
        milestones = [10, 25, 50, 100, 250, 500]
        for milestone in milestones:
            if completed_count == milestone:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO achievements
                    (student_id, achievement_type, achievement_name)
                    VALUES (?, 'milestone', ?)
                """,
                    (self.student_id, f"{milestone} Algorithms Completed"),
                )

        self.conn.commit()

    def close(self):
        """Close database connection."""
        self.conn.close()


if __name__ == "__main__":
    # Example usage
    tracker = StudentProgressTracker("student_001")
    tracker.start_algorithm(1)
    tracker.complete_algorithm(1, time_spent_minutes=30)
    tracker.record_test_result(1, 95.0, 10, 9)

    summary = tracker.get_progress_summary()
    print(json.dumps(summary, indent=2))

    tracker.close()
