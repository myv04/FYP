import sqlite3
from course_data import data_science_students

conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

course_id = 4  # Data Science

for student in data_science_students:
    cursor.execute('''
        INSERT OR IGNORE INTO students (
            id, username, attendance, exam_status, exam_score,
            a1_score, a1_status, a1_penalty,
            a2_score, a2_status, a2_penalty,
            status, enrollment_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        student["id"],  # Like "DS6846"
        student["name"],
        student["attendance"],
        student["exam_status"],
        student["exam_score"],
        student["a1_score"],
        student["a1_status"],
        student["a1_penalty"],
        student["a2_score"],
        student["a2_status"],
        student["a2_penalty"],
        student["status"],
        "Active"
    ))

    cursor.execute('''
        INSERT OR IGNORE INTO enrollments (student_id, course_id)
        VALUES (?, ?)
    ''', (student["id"], course_id))

conn.commit()
conn.close()
print("✅ Data Science students seeded successfully.")
