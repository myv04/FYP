import sqlite3
import random

# List of 50 protected IDs (those already in dashboards elsewhere)
protected_ids = set([
    'SE274186', 'SE239278', 'SE550110', 'SE406328', 'SE654033',
    'SE831216', 'SE371373', 'SE900421', 'SE880735', 'SE936782',
    # ⬆️ Add all 50 here (replace with real ones from SE dashboard if needed)
])

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# ✅ Step 1: Get 80 eligible SE students not in protected list
cursor.execute("""
SELECT id FROM students
WHERE id LIKE 'SE%' AND LOWER(role) = 'student'
AND id NOT IN (SELECT student_id FROM module_enrollments WHERE module_code = 'WS201')
""")

all_candidates = [row[0] for row in cursor.fetchall()]
eligible = [s for s in all_candidates if s not in protected_ids][:80]

print(f"Found {len(eligible)} eligible SE students. Linking to WS201...")

# ✅ Step 2: Enroll them and insert assignment data
for student_id in eligible:
    cursor.execute("""
        INSERT OR IGNORE INTO module_enrollments (student_id, module_code)
        VALUES (?, ?)
    """, (student_id, "WS201"))

    # Assign dummy assignment data (Assignment 1 for Web Tech)
    score = round(random.uniform(60, 95), 2)
    status = random.choice(["Completed", "Not Completed"])
    penalty = random.choice(["", "Lateness Penalty", "Word Count Penalty", "Both Penalties"])

    cursor.execute("""
        UPDATE students
        SET a1_score = ?, a1_status = ?, a1_penalty = ?
        WHERE id = ?
    """, (score, status, penalty, student_id))

conn.commit()
conn.close()
print("✅ 80 SE students safely enrolled in WS201 with assignment data.")
    