import sqlite3
import random
from faker import Faker

fake = Faker()
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Role-based configuration
role_config = [
    {"role": "Lecturer", "count": 30, "course_id": 3, "id_start": 800000},
    {"role": "Lecturer", "count": 25, "course_id": 4, "id_start": 800000},
    {"role": "TA",       "count": 5,  "course_id": 3, "id_start": 850000},
    {"role": "TA",       "count": 5,  "course_id": 4, "id_start": 850000},
    {"role": "Admin",    "count": 2,  "course_id": 3, "id_start": 900000},
    {"role": "Admin",    "count": 1,  "course_id": 4, "id_start": 900000},
    {"role": "Admin",    "count": 3,  "course_id": None, "id_start": 900000}
]

# Get used IDs to avoid duplicates
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

        # Insert into students table
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

        # Enroll in course if course_id exists
        if cfg["course_id"]:
            cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (user_id, cfg["course_id"]))

        inserted.append((user_id, name, cfg["role"], cfg["course_id"] or "Global"))

conn.commit()
conn.close()

print(f"✅ Inserted {len(inserted)} staff records successfully.")
