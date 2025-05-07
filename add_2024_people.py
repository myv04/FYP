import sqlite3
from datetime import datetime
import random

db_path = "courses.db"
software_course_id = 5  # SE100
today = datetime.today().strftime("%Y-%m-%d")

students_2024 = [
    ("SE1001", "Liam Carter", "liamcarter@uni.com"),
    ("SE1002", "Emma Davis", "emmadavis@uni.com"),
    ("SE1003", "Noah Smith", "noahsmith@uni.com"),
    ("SE1004", "Olivia Johnson", "oliviajohnson@uni.com"),
    ("SE1005", "Lucas Brown", "lucasbrown@uni.com"),
    ("SE1006", "Mia Wilson", "miawilson@uni.com"),
    ("SE1007", "Ethan Lee", "ethanlee@uni.com"),
    ("SE1008", "Ava Walker", "avawalker@uni.com"),
    ("SE1009", "James Scott", "jamesscott@uni.com"),
    ("SE1010", "Sophia Hill", "sophiahill@uni.com"),
]

lecturers_2024 = [
    ("91001", "Dr. Emily Roberts", "emilyroberts@uni.com"),
    ("91002", "Dr. Daniel Lewis", "daniellewis@uni.com"),
    ("91003", "Dr. Chloe Turner", "chloeturner@uni.com"),
    ("91004", "Dr. Joshua White", "joshuawhite@uni.com"),
    ("91005", "Dr. Lily Green", "lilygreen@uni.com"),
]

tas_2024 = [
    ("92001", "TA Henry Adams", "henryadams@uni.com"),
    ("92002", "TA Grace Bennett", "gracebennett@uni.com"),
    ("92003", "TA Benjamin Evans", "benjaminevans@uni.com"),
    ("92004", "TA Zoey Ramirez", "zoeyramirez@uni.com"),
    ("92005", "TA Elijah Moore", "elijahmoore@uni.com"),
]

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

# Add them
insert_people(students_2024, "Student", software_course_id)
insert_people(lecturers_2024, "Lecturer", software_course_id)
insert_people(tas_2024, "Teacher Assistant", software_course_id)

print("✅ Added students, lecturers, and TAs to 2024 Software Engineering (SE100).")
