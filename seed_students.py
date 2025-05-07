import sqlite3
from course_data import data_science_students, software_engineering_students
from datetime import datetime

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

def insert_students(students):
    for student in students:
        cursor.execute('''
            INSERT OR REPLACE INTO students (
                id, username, email, role, join_date,
                attendance, exam_status, exam_score,
                a1_score, a1_status, a1_penalty,
                a2_score, a2_status, a2_penalty,
                status, enrollment_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student["id"],
            student["name"],
            f'{student["name"].replace(" ", "").lower()}@uni.com',
            "Student",
            datetime.now().strftime("%Y-%m-%d"),
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

insert_students(data_science_students)
insert_students(software_engineering_students)

conn.commit()
conn.close()
print("✅ Students successfully inserted into the database.")
