#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Populate database with algorithm metadata.
Scans all algorithm directories and extracts comprehensive information.
"""

import sqlite3
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

# Import classification function
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from classify_algorithm_types import classify_algorithm_type
except ImportError:
    # Fallback if import fails
    def classify_algorithm_type(name, lecture=None, content=None):
        return "fundamental"


def extract_semester_number(path: Path) -> Optional[int]:
    """Extract semester number from path."""
    parts = path.parts
    for part in parts:
        if part.startswith("semester_"):
            try:
                return int(part.split("_")[1])
            except:
                pass
    return None


def extract_metadata_from_readme(readme_path: Path) -> Dict:
    """Extract metadata from README.md."""
    metadata = {}

    if not readme_path.exists():
        return metadata

    try:
        content = readme_path.read_text(encoding="utf-8")

        # Extract time complexity
        time_match = re.search(r"\*\*Time Complexity\*\*:\s*(.+?)(?:\n|$)", content)
        if time_match:
            metadata["time_complexity"] = time_match.group(1).strip()

        # Extract space complexity
        space_match = re.search(r"\*\*Space Complexity\*\*:\s*(.+?)(?:\n|$)", content)
        if space_match:
            metadata["space_complexity"] = space_match.group(1).strip()

        # Extract category
        category_match = re.search(r"\*\*Category\*\*:\s*(.+?)(?:\n|$)", content)
        if category_match:
            metadata["category"] = category_match.group(1).strip()

        # Extract short description
        desc_match = re.search(
            r"### Short Description\s*\n\n(.+?)(?:\n\n|\n##)", content, re.DOTALL
        )
        if desc_match:
            metadata["short_description"] = desc_match.group(1).strip()[:500]

        # Extract description from Introduction
        intro_match = re.search(
            r"## Introduction\s*\n\n(.+?)(?:\n\n|\n##)", content, re.DOTALL
        )
        if intro_match:
            metadata["description"] = intro_match.group(1).strip()[:1000]

        # Extract stability
        stability_match = re.search(r"\*\*Stability\*\*:\s*(.+?)(?:\n|$)", content)
        if stability_match:
            metadata["stability"] = stability_match.group(1).strip()

        # Extract advantages
        advantages = []
        if "## Key Advantages" in content or "**Advantages**" in content:
            adv_section = re.search(
                r"(?:## Key Advantages|## Advantages|### Advantages)\s*\n\n(.+?)(?:\n\n##|\n## Key|$)",
                content,
                re.DOTALL,
            )
            if adv_section:
                lines = adv_section.group(1).split("\n")
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith("-") or line.startswith("*")):
                        advantages.append(line.lstrip("-* ").strip())
        metadata["advantages"] = advantages[:10]  # Limit to 10

        # Extract shortcomings
        shortcomings = []
        if "## Key Disadvantages" in content or "**Disadvantages**" in content:
            dis_section = re.search(
                r"(?:## Key Disadvantages|## Disadvantages|### Disadvantages)\s*\n\n(.+?)(?:\n\n##|\n## Key|$)",
                content,
                re.DOTALL,
            )
            if dis_section:
                lines = dis_section.group(1).split("\n")
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith("-") or line.startswith("*")):
                        shortcomings.append(line.lstrip("-* ").strip())
        metadata["shortcomings"] = shortcomings[:10]  # Limit to 10

        # Extract framework usage
        frameworks = []
        if "## Examples of Implementation" in content:
            framework_section = re.search(
                r"## Examples of Implementation\s*\n\n(.+?)(?:\n\n##|$)",
                content,
                re.DOTALL,
            )
            if framework_section:
                # Extract framework names
                framework_names = re.findall(
                    r"### (.+? Framework|Docker|Kubernetes|Apache Kafka|Nginx)",
                    framework_section.group(1),
                )
                frameworks = [
                    name.replace(" Framework", "") for name in framework_names
                ]
        metadata["frameworks"] = frameworks

    except Exception as e:
        print(f"Error reading {readme_path}: {e}")

    return metadata


def get_file_info(file_path: Path) -> Dict:
    """Get file information."""
    if not file_path.exists():
        return {}

    stat = file_path.stat()
    return {
        "size": stat.st_size,
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }


def create_schema(cursor):
    """Create database schema."""
    # Create tables
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS algorithms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            display_name TEXT NOT NULL,
            folder_path TEXT NOT NULL,
            semester_number INTEGER,
            lecture_name TEXT,
            category TEXT,
            algorithm_type TEXT,
            description TEXT,
            short_description TEXT,
            time_complexity TEXT,
            space_complexity TEXT,
            stability TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    
    # Add algorithm_type column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE algorithms ADD COLUMN algorithm_type TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS algorithm_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_id INTEGER NOT NULL,
            file_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_size INTEGER,
            last_modified TIMESTAMP,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE,
            UNIQUE(algorithm_id, file_type)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_id INTEGER NOT NULL,
            test_file_path TEXT NOT NULL,
            test_count INTEGER DEFAULT 0,
            coverage_percentage REAL DEFAULT 0.0,
            last_run TIMESTAMP,
            status TEXT,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_id INTEGER NOT NULL,
            input_size INTEGER NOT NULL,
            execution_time_ms REAL,
            memory_usage_mb REAL,
            operations_per_sec REAL,
            language TEXT,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS framework_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_id INTEGER NOT NULL,
            framework_name TEXT NOT NULL,
            framework_type TEXT,
            example_code TEXT,
            purpose TEXT,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE,
            UNIQUE(algorithm_id, framework_name)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS algorithm_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_id INTEGER NOT NULL,
            usage_count INTEGER DEFAULT 0,
            last_used TIMESTAMP,
            usage_context TEXT,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS algorithm_advantages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_id INTEGER NOT NULL,
            advantage TEXT NOT NULL,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS algorithm_shortcomings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_id INTEGER NOT NULL,
            shortcoming TEXT NOT NULL,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
        )
    """
    )

    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_algorithms_name ON algorithms(name)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_algorithms_semester ON algorithms(semester_number)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_algorithms_category ON algorithms(category)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_files_algorithm ON algorithm_files(algorithm_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_tests_algorithm ON test_files(algorithm_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_performance_algorithm ON performance_metrics(algorithm_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_framework_algorithm ON framework_usage(algorithm_id)"
    )


def populate_database():
    """Populate database with algorithm information."""
    # Create database directory
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create schema
    create_schema(cursor)
    conn.commit()

    # Find all algorithm directories
    algorithms_processed = 0
    for algo_dir in ROOT.rglob("*/algorithm.py"):
        algo_dir = algo_dir.parent
        algorithm_name = algo_dir.name

        if not (algo_dir / "README.md").exists():
            continue

        try:
            # Extract basic info
            semester_num = extract_semester_number(algo_dir)
            lecture_path = algo_dir.parent
            lecture_name = lecture_path.name if lecture_path else None

            # Extract metadata from README
            readme_metadata = extract_metadata_from_readme(algo_dir / "README.md")

            # Read metadata.json if exists
            metadata_json = {}
            metadata_file = algo_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    metadata_json = json.loads(
                        metadata_file.read_text(encoding="utf-8")
                    )
                except:
                    pass

            # Merge metadata
            category = (
                readme_metadata.get("category")
                or metadata_json.get("category")
                or "algorithm"
            )
            algorithm_type = (
                metadata_json.get("algorithm_type")
                or readme_metadata.get("algorithm_type")
                or classify_algorithm_type(algorithm_name, lecture_name, description)
            )
            description = (
                readme_metadata.get("description")
                or metadata_json.get("description")
                or ""
            )
            short_desc = readme_metadata.get("short_description") or ""

            # Insert or update algorithm
            cursor.execute(
                """
                INSERT OR REPLACE INTO algorithms 
                (name, display_name, folder_path, semester_number, lecture_name, category,
                 algorithm_type, description, short_description, time_complexity, space_complexity, stability, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    algorithm_name,
                    algorithm_name.replace("_", " ").title(),
                    str(algo_dir.relative_to(ROOT)),
                    semester_num,
                    lecture_name,
                    category,
                    algorithm_type,
                    description,
                    short_desc,
                    readme_metadata.get("time_complexity", "N/A"),
                    readme_metadata.get("space_complexity", "N/A"),
                    readme_metadata.get("stability", "N/A"),
                    datetime.now().isoformat(),
                ),
            )

            algorithm_id = cursor.lastrowid

            # Insert algorithm files
            files_to_check = [
                ("python", algo_dir / "algorithm.py"),
                ("java", algo_dir / "Algorithm.java"),
                ("sql", algo_dir / "algorithm.sql"),
                ("readme", algo_dir / "README.md"),
            ]

            for file_type, file_path in files_to_check:
                if file_path.exists():
                    file_info = get_file_info(file_path)
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO algorithm_files
                        (algorithm_id, file_type, file_path, file_name, file_size, last_modified)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            algorithm_id,
                            file_type,
                            str(file_path.relative_to(ROOT)),
                            file_path.name,
                            file_info.get("size", 0),
                            file_info.get("last_modified"),
                        ),
                    )

            # Insert test file
            test_file = algo_dir / "test_algorithm.py"
            if test_file.exists():
                # Count test methods
                test_content = test_file.read_text(encoding="utf-8")
                test_count = len(re.findall(r"def\s+test_", test_content))

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO test_files
                    (algorithm_id, test_file_path, test_count, status)
                    VALUES (?, ?, ?, ?)
                """,
                    (
                        algorithm_id,
                        str(test_file.relative_to(ROOT)),
                        test_count,
                        "not_run",
                    ),
                )

            # Insert advantages
            for advantage in readme_metadata.get("advantages", [])[:10]:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO algorithm_advantages (algorithm_id, advantage)
                    VALUES (?, ?)
                """,
                    (algorithm_id, advantage),
                )

            # Insert shortcomings
            for shortcoming in readme_metadata.get("shortcomings", [])[:10]:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO algorithm_shortcomings (algorithm_id, shortcoming)
                    VALUES (?, ?)
                """,
                    (algorithm_id, shortcoming),
                )

            # Insert framework usage
            for framework in readme_metadata.get("frameworks", []):
                framework_type = (
                    "java"
                    if framework in ["Spring", "J2EE"]
                    else (
                        "csharp"
                        if framework == ".NET"
                        else (
                            "yaml"
                            if framework in ["Docker", "Kubernetes"]
                            else "python" if framework == "Kafka" else "other"
                        )
                    )
                )

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO framework_usage
                    (algorithm_id, framework_name, framework_type)
                    VALUES (?, ?, ?)
                """,
                    (algorithm_id, framework, framework_type),
                )

            # Initialize usage tracking
            cursor.execute(
                """
                INSERT OR IGNORE INTO algorithm_usage (algorithm_id, usage_count)
                VALUES (?, 0)
            """,
                (algorithm_id,),
            )

            algorithms_processed += 1
            if algorithms_processed % 50 == 0:
                print(f"[PROGRESS] Processed {algorithms_processed} algorithms...")
                conn.commit()

        except Exception as e:
            print(f"Error processing {algo_dir}: {e}")
            continue

    conn.commit()

    # Get statistics (using direct query since view might not exist)
    cursor.execute(
        """
        SELECT 
            COUNT(DISTINCT a.id) as total_algorithms,
            COUNT(DISTINCT a.semester_number) as total_semesters,
            COUNT(DISTINCT a.category) as total_categories,
            COUNT(DISTINCT CASE WHEN af.file_type = 'python' THEN af.id END) as python_files,
            COUNT(DISTINCT CASE WHEN af.file_type = 'java' THEN af.id END) as java_files,
            COUNT(DISTINCT CASE WHEN af.file_type = 'sql' THEN af.id END) as sql_files,
            COUNT(DISTINCT tf.id) as total_tests,
            COUNT(DISTINCT fw.id) as total_framework_examples
        FROM algorithms a
        LEFT JOIN algorithm_files af ON a.id = af.algorithm_id
        LEFT JOIN test_files tf ON a.id = tf.algorithm_id
        LEFT JOIN framework_usage fw ON a.id = fw.algorithm_id
    """
    )
    stats = cursor.fetchone()

    print(f"\n[COMPLETE] Processed {algorithms_processed} algorithms")
    print(f"Database saved to: {DB_PATH}")
    if stats:
        print(
            f"Statistics: {stats[0]} algorithms, {stats[1]} semesters, {stats[2]} categories"
        )

    conn.close()
    return algorithms_processed


if __name__ == "__main__":
    populate_database()
