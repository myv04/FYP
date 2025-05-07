import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

def random_name():
    return random.choice(["Alex", "Taylor", "Jordan", "Morgan", "Casey", "Riley", "Skyler", "Cameron"]) + " " + \
           random.choice(["Smith", "Johnson", "Davis", "Lee", "Clark", "Brown", "Wilson", "Anderson"])

def random_penalty():
    return random.choice(["None", "Lateness Penalty", "Word Count Penalty", "None"])

def random_join_date():
    start = datetime.strptime("2024-09-01", "%Y-%m-%d")
    end = datetime.strptime("2024-10-15", "%Y-%m-%d")
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

# Select students missing any key data field
cursor.execute("""
    SELECT id, username FROM students
    WHERE a1_score IS NULL OR a2_score IS NULL OR exam_score IS NULL
       OR a1_status IS NULL OR a2_status IS NULL OR exam_status IS NULL
       OR attendance IS NULL OR status IS NULL OR enrollment_status IS NULL
       OR role IS NULL OR join_date IS NULL OR email IS NULL OR uni_id IS NULL
""")

students_to_patch = cursor.fetchall()

for sid, name in students_to_patch:
    a1_score = random.randint(50, 95)
    a2_score = random.randint(50, 95)
    exam_score = random.randint(40, 90)
    attendance = random.randint(60, 100)
    a1_status = "Completed"
    a2_status = "Completed"
    exam_status = "Fit to Sit"
    a1_penalty = random_penalty()
    a2_penalty = random_penalty()
    status = "Active"
    enrollment_status = "Enrolled"
    role = "student"
    join_date = random_join_date()
    email = f"{name.replace(' ', '').lower()}@autopatch.edu"
    uni_id = sid  # Use the student ID as uni_id

    cursor.execute("""
        UPDATE students
        SET a1_score = ?, a2_score = ?, exam_score = ?,
            a1_status = ?, a2_status = ?, exam_status = ?,
            a1_penalty = ?, a2_penalty = ?, attendance = ?,
            status = ?, enrollment_status = ?, role = ?,
            join_date = ?, email = ?, uni_id = ?
        WHERE id = ?
    """, (
        a1_score, a2_score, exam_score,
        a1_status, a2_status, exam_status,
        a1_penalty, a2_penalty, attendance,
        status, enrollment_status, role,
        join_date, email, uni_id, sid
    ))

conn.commit()
conn.close()

print(f"✅ Patched {len(students_to_patch)} students with missing data.")
