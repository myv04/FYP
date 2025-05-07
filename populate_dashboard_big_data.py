import sqlite3
from datetime import datetime

conn = sqlite3.connect("instance/database.db")
cursor = conn.cursor()

sample_students = [
    {
        "id": "DS6846", "student": "Alex Carter", "final_grade": 76, "attendance": 81,
        "assignment_1_score": 59, "assignment_1_status": "Completed", "assignment_1_penalty": "",
        "status": "Enrolled"
    },
    {
        "id": "DS6478", "student": "Bella Sanders", "final_grade": 82, "attendance": 88,
        "assignment_1_score": 72, "assignment_1_status": "Completed", "assignment_1_penalty": "Late Submission",
        "status": "Enrolled"
    },
    {
        "id": "DS9754", "student": "Diana Wright", "final_grade": 90, "attendance": 92,
        "assignment_1_score": 89, "assignment_1_status": "Completed", "assignment_1_penalty": "",
        "status": "Enrolled"
    }
]

for student in sample_students:
    cursor.execute("""
        INSERT OR REPLACE INTO dashboard_big_data 
        (id, student, "Final Grade", "Attendance (%)",
         "Assignment 1 (Data Lakes)", "Assignment 1 Status", "Assignment 1 Penalty", status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student["id"], student["student"], student["final_grade"], student["attendance"],
        student["assignment_1_score"], student["assignment_1_status"], student["assignment_1_penalty"],
        student["status"]
    ))

conn.commit()
conn.close()

print("✅ Inserted sample students into dashboard_big_data (DS102).")
