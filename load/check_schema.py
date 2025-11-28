"""Check if database has all required columns."""
import sqlite3
from pathlib import Path

db_path = Path("../algos.db")
if not db_path.exists():
    db_path = Path("algos.db")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(algorithm_descriptions)")
columns = {row[1]: row[2] for row in cursor.fetchall()}

print("Existing columns in algorithm_descriptions:")
for col in sorted(columns.keys()):
    print(f"  - {col}")

required_columns = {
    'simple_explanation': 'School level - Simple Explanation',
    'where_its_used': 'School level - Where It\'s Used',
    'example': 'School level - Example',
    'algorithm_definition': 'University level - Algorithm Definition',
    'technical_description': 'University level - Technical Description',
    'application': 'University level - Application',
    'step_by_step': 'University level - Step-by-Step'
}

print("\n" + "="*60)
print("Required columns check:")
print("="*60)

missing = []
for col, desc in required_columns.items():
    if col in columns:
        print(f"✓ {col} - {desc}")
    else:
        print(f"✗ {col} - {desc} - MISSING!")
        missing.append(col)

if missing:
    print(f"\n⚠️  Missing columns: {missing}")
    print("\nRun the ALTER TABLE statements from createDbSql.txt to add them.")
else:
    print("\n✅ All required columns exist!")

conn.close()

