import sqlite3
import random
from datetime import datetime, timedelta

# Connect to your local courses.db
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Make sure enrollments table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    student_id TEXT,
    course_id INTEGER,
    PRIMARY KEY (student_id, course_id)
)
""")

# Helpers
def random_name():
    first = random.choice(["Alex", "Taylor", "Jordan", "Morgan", "Casey", "Riley", "Skyler", "Cameron"])
    last = random.choice(["Smith", "Johnson", "Davis", "Lee", "Clark", "Brown", "Wilson", "Anderson"])
    return f"{first} {last}"

def random_penalty():
    return random.choice(["None", "Lateness Penalty", "Word Count Penalty", "None", "None"])

def random_join_date():
    start = datetime.strptime("2024-09-01", "%Y-%m-%d")
    end = datetime.strptime("2024-10-15", "%Y-%m-%d")
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

# Master data list
students = []
enrollments = []

# 500 SE101 students
for i in range(500):
    sid = f"SE{i+100000}"
    name = random_name()
    email = f"{name.replace(' ', '').lower()}{i}@se101.edu"
    a1_score = random.randint(50, 95)
    a2_score = random.randint(50, 95)
    exam_score = random.randint(40, 90)
    attendance = random.randint(60, 100)
    join_date = random_join_date()

    student = (
        sid, name, attendance,
        "Fit to Sit", exam_score,
        a1_score, "Completed", random_penalty(),
        a2_score, "Completed", random_penalty(),
        "Active", "Enrolled", "student",
        join_date, email, sid
    )
    students.append(student)
    enrollments.append((sid, 3))  # SE101 = course_id 3

# 450 DS102 students
for i in range(450):
    sid = f"DS{i+100000}"
    name = random_name()
    email = f"{name.replace(' ', '').lower()}{i}@ds102.edu"
    a1_score = random.randint(50, 95)
    a2_score = random.randint(50, 95)
    exam_score = random.randint(40, 90)
    attendance = random.randint(60, 100)
    join_date = random_join_date()

    student = (
        sid, name, attendance,
        "Fit to Sit", exam_score,
        a1_score, "Completed", random_penalty(),
        a2_score, "Completed", random_penalty(),
        "Active", "Enrolled", "student",
        join_date, email, sid
    )
    students.append(student)
    enrollments.append((sid, 4))  # DS102 = course_id 4

# Insert into DB
cursor.executemany("""
INSERT OR REPLACE INTO students (
    id, username, attendance,
    exam_status, exam_score,
    a1_score, a1_status, a1_penalty,
    a2_score, a2_status, a2_penalty,
    status, enrollment_status, role,
    join_date, email, uni_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", students)

cursor.executemany("INSERT OR REPLACE INTO enrollments (student_id, course_id) VALUES (?, ?)", enrollments)


conn.commit()
conn.close()

print("✅ 950 students successfully created and enrolled.")
