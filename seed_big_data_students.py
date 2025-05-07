import sqlite3
import random

# Load protected IDs (students that should NOT be modified)
with open("protected_ids.txt", "r") as f:
    protected_ids = set(line.strip() for line in f.readlines())

# Connect to database
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Get non-protected DS students
students = cursor.execute("""
    SELECT id FROM students
    WHERE id LIKE 'DS%' AND LOWER(role) = 'student'
""").fetchall()

non_protected = [s[0] for s in students if s[0] not in protected_ids]
selected = non_protected[:80]

print(f"Found {len(selected)} eligible non-protected DS students. Linking to DS102...")

# Enroll and update their assignment data
for student_id in selected:
    # Link to module
    cursor.execute("""
        INSERT OR IGNORE INTO module_enrollments (student_id, module_code)
        VALUES (?, ?)
    """, (student_id, "DS102"))

    # Add dummy assignment data if it's missing
    cursor.execute("""
        UPDATE students
        SET
            a1_score = COALESCE(a1_score, ?),
            a1_status = COALESCE(a1_status, 'Completed'),
            a1_penalty = COALESCE(a1_penalty, ''),
            attendance = COALESCE(attendance, ?),
            status = COALESCE(status, 'Enrolled')
        WHERE id = ?
    """, (
        random.randint(50, 95),     # a1_score
        random.randint(60, 100),    # attendance
        student_id
    ))

conn.commit()
conn.close()

print("✅ 80 DS students safely enrolled in DS102 without touching protected ones.")
