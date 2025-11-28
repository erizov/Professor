"""Quick script to query the database."""
import sqlite3
from pathlib import Path

# Find database file
db_path = Path("algos.db")
if not db_path.exists():
    db_path = Path("../algos.db")
if not db_path.exists():
    print(f"Database not found. Looking for: {db_path.absolute()}")
    exit(1)

print(f"Database location: {db_path.absolute()}\n")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get total count
cursor.execute("SELECT COUNT(*) FROM algorithm_descriptions")
total = cursor.fetchone()[0]
print(f"Total records: {total}\n")

# Get top 50 most recent
cursor.execute("""
    SELECT algorithm_name, language, level, title, source_site, fetched_at 
    FROM algorithm_descriptions 
    ORDER BY fetched_at DESC 
    LIMIT 50
""")

rows = cursor.fetchall()
print("Top 50 records (most recent first):")
print("=" * 120)
print(f"{'#':<4} {'Algorithm':<30} {'Lang':<5} {'Level':<12} {'Title':<40} {'Source':<20} {'Fetched At'}")
print("=" * 120)

for i, row in enumerate(rows, 1):
    algo_name = row[0][:28] if row[0] else "N/A"
    lang = row[1] or "N/A"
    level = row[2] or "N/A"
    title = (row[3][:38] + "..") if row[3] and len(row[3]) > 40 else (row[3] or "N/A")
    source = row[4] or "N/A"
    fetched = str(row[5])[:19] if row[5] else "N/A"
    print(f"{i:<4} {algo_name:<30} {lang:<5} {level:<12} {title:<40} {source:<20} {fetched}")

conn.close()

