"""
Clean up incorrect algorithm entries from database.
Removes entries that are clearly not algorithms (cars, organizations, etc.)
"""
import sqlite3
from pathlib import Path
import re

# Database path
db_path = Path("../algos.db")
if not db_path.exists():
    db_path = Path("algos.db")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Find incorrect entries
incorrect_patterns = [
    '%Jaguar%',
    '%XK140%',
    '%Талибан%',
    '%Taliban%',
    '%Tehrik%',
    '%Пакистан%'
]

print("Searching for incorrect entries...")
incorrect_entries = []

for pattern in incorrect_patterns:
    cursor.execute("""
        SELECT id, algorithm_name, title, source_site, language, level
        FROM algorithm_descriptions
        WHERE title LIKE ? OR algorithm_name LIKE ?
    """, (pattern, pattern))
    rows = cursor.fetchall()
    incorrect_entries.extend(rows)

# Remove duplicates
incorrect_entries = list(set(incorrect_entries))

if incorrect_entries:
    print(f"\nFound {len(incorrect_entries)} incorrect entries:")
    for entry in incorrect_entries:
        print(f"  ID: {entry[0]}, Algorithm: {entry[1]}, Title: {entry[2]}, Source: {entry[3]}")
    
    print("\nDeleting incorrect entries...")
    for entry in incorrect_entries:
        entry_id = entry[0]
        cursor.execute("DELETE FROM algorithm_descriptions WHERE id = ?", (entry_id,))
        print(f"  Deleted entry ID {entry_id}: {entry[2]}")
    
    conn.commit()
    print(f"\n✓ Deleted {len(incorrect_entries)} incorrect entries")
else:
    print("No incorrect entries found.")

# Also check for algorithm names that might be incorrect
print("\nChecking for suspicious algorithm names...")
cursor.execute("""
    SELECT DISTINCT algorithm_name, COUNT(*) as count
    FROM algorithm_descriptions
    GROUP BY algorithm_name
    HAVING COUNT(*) < 2
""")
suspicious = cursor.fetchall()

non_algorithm_keywords = [
    'jaguar', 'xk140', 'taliban', 'талибан', 'pakistan', 'пакистан',
    'car', 'автомобиль', 'organization', 'организация'
]

suspicious_entries = []
for algo_name, count in suspicious:
    if any(keyword in algo_name.lower() for keyword in non_algorithm_keywords):
        suspicious_entries.append(algo_name)

if suspicious_entries:
    print(f"\nFound {len(suspicious_entries)} suspicious algorithm names:")
    for name in suspicious_entries:
        print(f"  - {name}")
        cursor.execute("DELETE FROM algorithm_descriptions WHERE algorithm_name = ?", (name,))
        cursor.execute("DELETE FROM algorithms WHERE algorithm_name = ?", (name,))
    conn.commit()
    print(f"✓ Cleaned up {len(suspicious_entries)} suspicious entries")

conn.close()
print("\nCleanup complete!")

