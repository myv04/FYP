import sqlite3
from datetime import datetime
import random

db_path = "courses.db"
course_id_ds = 6  # DS101
today = datetime.today().strftime("%Y-%m-%d")

def generate_people(start_id, prefix, count, name_prefix):
    return [
        (f"{prefix}{start_id + i}", f"{name_prefix} {i+1}", f"{name_prefix.lower()}{i+1}@uni.com")
        for i in range(count)
    ]

# Data Science cohort
students_ds = generate_people(1001, "DS", 10, "DS_Student")
lecturers_ds = generate_people(9101, "", 5, "DS_Lecturer")
tas_ds = generate_people(9201, "", 5, "DS_TA")

def insert_people(people, role, course_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for uid, name, email in people:
        cursor.execute("""
            INSERT OR REPLACE INTO students (
                id, username, attendance, exam_status, exam_score, a1_score, a1_status,
                a1_penalty, a2_score, a2_status, a2_penalty, enrollment_status, role,
                join_date, email, uni_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uid, name, random.randint(70, 100), "Fit to Sit", random.randint(60, 100),
            random.randint(60, 100), "Completed", "", random.randint(60, 100), "Completed", "",
            "Enrolled", role, today, email, uid
        ))

        cursor.execute("""
            INSERT OR REPLACE INTO enrollments (student_id, course_id)
            VALUES (?, ?)
        """, (uid, course_id))

    conn.commit()
    conn.close()

# Insert DS cohort
insert_people(students_ds, "Student", course_id_ds)
insert_people(lecturers_ds, "Lecturer", course_id_ds)
insert_people(tas_ds, "Teacher Assistant", course_id_ds)

print("✅ Data Science 2024 (DS101) — Students, Lecturers, and TAs added.")
