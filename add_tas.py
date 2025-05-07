import sqlite3
import random
from faker import Faker

fake = Faker()
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Only TA roles for SE (3) and DS (4)
role_config = [
    {"role": "TA", "count": 10, "course_id": 3, "id_start": 850000},
    {"role": "TA", "count": 10, "course_id": 4, "id_start": 850000}
]

cursor.execute("SELECT id FROM students")
existing_ids = set(row[0] for row in cursor.fetchall())

def generate_unique_id(start_range, used_ids):
    while True:
        new_id = str(random.randint(start_range, start_range + 9999))
        if new_id not in used_ids:
            used_ids.add(new_id)
            return new_id

join_date = "2025-09-10"
enrollment_status = "Enrolled"

inserted = []

for cfg in role_config:
    for _ in range(cfg["count"]):
        user_id = generate_unique_id(cfg["id_start"], existing_ids)
        name = fake.name()
        email = f"{name.lower().replace(' ', '.')}@uni.com"

        cursor.execute("""
            INSERT INTO students (
                id, username, attendance, exam_status, exam_score,
                a1_score, a1_status, a1_penalty,
                a2_score, a2_status, a2_penalty,
                enrollment_status, role, join_date, email, uni_id
            ) VALUES (?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                      ?, ?, ?, ?, ?)
        """, (
            user_id, name, enrollment_status, cfg["role"],
            join_date, email, user_id
        ))

        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (user_id, cfg["course_id"]))
        inserted.append((user_id, name, cfg["role"], cfg["course_id"]))

conn.commit()
conn.close()

print(f"✅ Successfully added {len(inserted)} new TA accounts.")
