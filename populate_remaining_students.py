import sqlite3
import random
from faker import Faker

fake = Faker()

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Course targets
targets = {
    3: 500,  # SE101
    4: 450   # DS102
}
prefix_map = {
    3: "SE",
    4: "DS"
}
join_date = "2025-09-15"
role = "Student"
enrollment_status = "Enrolled"
status = "Active"

# Get current student IDs
cursor.execute("SELECT id FROM students")
existing_ids = set(row[0] for row in cursor.fetchall())

# Count current enrollments per course
cursor.execute("""
    SELECT course_id, COUNT(*) FROM enrollments
    GROUP BY course_id
""")
current = {row[0]: row[1] for row in cursor.fetchall()}

# Track students added
added = []

def generate_unique_id(prefix):
    while True:
        sid = f"{prefix}{random.randint(100000, 999999)}"
        if sid not in existing_ids:
            existing_ids.add(sid)
            return sid

for course_id, target in targets.items():
    current_count = current.get(course_id, 0)
    to_add = target - current_count
    prefix = prefix_map[course_id]

    for _ in range(to_add):
        sid = generate_unique_id(prefix)
        name = fake.name()
        username = name
        email = f"{name.lower().replace(' ', '')}{sid}@uni.com"

        student_data = (
            sid, username, random.randint(60, 100),  # attendance
            "Fit to Sit", random.randint(50, 95),    # exam
            random.randint(50, 95), "Completed", "", # a1
            random.randint(50, 95), "Completed", "", # a2
            status, enrollment_status, role,
            join_date, email, sid
        )

        cursor.execute("""
            INSERT INTO students (
                id, username, attendance, exam_status, exam_score,
                a1_score, a1_status, a1_penalty,
                a2_score, a2_status, a2_penalty,
                status, enrollment_status, role,
                join_date, email, uni_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, student_data)

        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (sid, course_id))
        added.append((sid, username, course_id))

conn.commit()
conn.close()

print(f"✅ Successfully added {len(added)} new students.")
