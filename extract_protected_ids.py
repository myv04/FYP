# extract_protected_ids.py
import sqlite3

# Connect to your database
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Get 50 students with a1_score already filled (used in old dashboard)
cursor.execute("""
    SELECT id FROM students
    WHERE a1_score IS NOT NULL
    AND id LIKE 'DS%'
    ORDER BY id
    LIMIT 50
""")

rows = cursor.fetchall()

# Save them to a text file for protection
with open("protected_ids.txt", "w") as f:
    for (student_id,) in rows:
        f.write(student_id + "\n")

conn.close()
print("✅ Saved protected student IDs to protected_ids.txt")
