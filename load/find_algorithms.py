"""Find algorithms related to the deleted entries."""
import sqlite3
from pathlib import Path

db_path = Path("../algos.db")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Search for related algorithms
cursor.execute("""
    SELECT DISTINCT algorithm_name, canonical_label
    FROM algorithms
    WHERE algorithm_name LIKE '%conditional%' 
       OR algorithm_name LIKE '%model%'
       OR algorithm_name LIKE '%registry%'
       OR canonical_label LIKE '%conditional%'
       OR canonical_label LIKE '%model%'
       OR canonical_label LIKE '%registry%'
""")

rows = cursor.fetchall()
print("Related algorithms found:")
for algo_name, canonical in rows:
    print(f"  {algo_name} -> {canonical}")
    
    # Check how many descriptions exist
    cursor.execute("""
        SELECT COUNT(*) FROM algorithm_descriptions 
        WHERE algorithm_name = ?
    """, (algo_name,))
    count = cursor.fetchone()[0]
    print(f"    Descriptions: {count}")

conn.close()

