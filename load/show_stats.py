"""Show database statistics."""
import sqlite3
from pathlib import Path

# Find database file
db_path = Path("algos.db")
if not db_path.exists():
    db_path = Path("../algos.db")

print(f"Database: {db_path.absolute()}\n")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Total algorithms
cursor.execute("SELECT COUNT(DISTINCT algorithm_name) FROM algorithms")
total_algorithms = cursor.fetchone()[0]
print(f"Total algorithms: {total_algorithms}")

# Total descriptions
cursor.execute("SELECT COUNT(*) FROM algorithm_descriptions")
total_descriptions = cursor.fetchone()[0]
print(f"Total descriptions: {total_descriptions}")

# By source
cursor.execute("""
    SELECT source_site, COUNT(*) 
    FROM algorithm_descriptions 
    GROUP BY source_site
""")
print("\nBy source:")
for row in cursor.fetchall():
    print(f"  {row[0] or 'NULL'}: {row[1]}")

# By language
cursor.execute("""
    SELECT language, COUNT(*) 
    FROM algorithm_descriptions 
    GROUP BY language
""")
print("\nBy language:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# By level
cursor.execute("""
    SELECT level, COUNT(*) 
    FROM algorithm_descriptions 
    GROUP BY level
""")
print("\nBy level:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Web vs local
cursor.execute("""
    SELECT 
        COUNT(*) FILTER (WHERE source_site != 'local_markdown') as web_count,
        COUNT(*) FILTER (WHERE source_site = 'local_markdown') as local_count
    FROM algorithm_descriptions
""")
row = cursor.fetchone()
print(f"\nWeb descriptions: {row[0]}")
print(f"Local descriptions: {row[1]}")

conn.close()

