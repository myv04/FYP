import sqlite3
import random

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# 1. Fetch all SE101 students
cursor.execute("""
    SELECT s.id, s.username
    FROM students s
    JOIN enrollments e ON s.id = e.student_id
    WHERE e.course_id = 'SE101' AND s.enrollment_status != 'Removed'
""")
all_students = cursor.fetchall()

# 2. Get existing hardcoded 50 student IDs from course_data.py
existing_ids = {
    "SE8946", "SE5918", "SE7494", "SE1509", "SE8253", "SE1744", "SE5043", "SE8979", "SE1968", "SE1852",
    "SE8330", "SE8811", "SE9771", "SE5353", "SE1179", "SE5838", "SE4247", "SE4796", "SE3642", "SE3570",
    "SE3688", "SE9940", "SE5462", "SE4267", "SE2196", "SE3056", "SE3902", "SE5236", "SE9158", "SE8950",
    "SE1967", "SE8256", "SE4532", "SE1517", "SE7469", "SE8148", "SE1419", "SE6287", "SE3159", "SE3655",
    "SE9723", "SE9035", "SE9083", "SE2110", "SE6193", "SE4227", "SE1890", "SE1314", "SE5890", "SE3935"
}

# 3. Filter to only those not in the existing 50
new_students = [s for s in all_students if s[0] not in existing_ids]

print(f"Found {len(new_students)} SE101 students not in course_data.py")

# 4. Randomly pick 80
selected = random.sample(new_students, 80)

# 5. Insert into WS201
inserted = 0
for student_id, _ in selected:
    try:
        # Assign assignment score/status/penalty randomly for realism
        a1_score = random.randint(50, 95)
        a1_status = "Completed"
        a1_penalty = random.choice(["", "", "", "Lateness Penalty", "Word Count Penalty"])  # Mostly clean

        cursor.execute("""
            INSERT OR IGNORE INTO module_enrollments (student_id, module_code)
            VALUES (?, ?)
        """, (student_id, "WS201"))

        cursor.execute("""
            UPDATE students
            SET a1_score = ?, a1_status = ?, a1_penalty = ?
            WHERE id = ?
        """, (a1_score, a1_status, a1_penalty, student_id))

        inserted += 1
    except Exception as e:
        print(f"⚠️ Failed to insert {student_id}: {e}")

conn.commit()
conn.close()
print(f"✅ {inserted} SE101 students enrolled into WS201 with assignment data.")
