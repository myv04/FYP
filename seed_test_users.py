import sqlite3
import uuid
from datetime import datetime

def generate_user(role, prefix, index):
    uni_id = f"{prefix}_TEST{str(index).zfill(3)}"
    return {
        "id": str(uuid.uuid4())[:8],
        "username": uni_id,
        "attendance": 0,
        "exam_status": "Not Started",
        "exam_score": 0,
        "a1_score": 0,
        "a1_status": "Not Submitted",
        "a1_penalty": "None",
        "a2_score": 0,
        "a2_status": "Not Submitted",
        "a2_penalty": "None",
        "status": "Active",
        "enrollment_status": "Pending",
        "role": role,
        "join_date": datetime.now().strftime("%Y-%m-%d"),
        "email": f"{uni_id.lower()}@test.edu",
        "uni_id": uni_id
    }

def add_unassigned_test_users(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    se_students = [generate_user("Student", "SE", i+1) for i in range(50)]
    ds_students = [generate_user("Student", "DS", i+1) for i in range(50)]
    se_lecturers = [generate_user("Lecturer", "SE", i+1) for i in range(10)]
    ds_lecturers = [generate_user("Lecturer", "DS", i+1) for i in range(10)]

    all_users = se_students + ds_students + se_lecturers + ds_lecturers

    for user in all_users:
        cur.execute("""
            INSERT INTO students (id, username, attendance, exam_status, exam_score, a1_score,
                                  a1_status, a1_penalty, a2_score, a2_status, a2_penalty, status,
                                  enrollment_status, role, join_date, email, uni_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user["id"], user["username"], user["attendance"], user["exam_status"], user["exam_score"],
            user["a1_score"], user["a1_status"], user["a1_penalty"], user["a2_score"],
            user["a2_status"], user["a2_penalty"], user["status"], user["enrollment_status"],
            user["role"], user["join_date"], user["email"], user["uni_id"]
        ))

    conn.commit()
    conn.close()
    print("✅ Test users added: 50 SE students, 50 DS students, 10 SE lecturers, 10 DS lecturers")

# Run it
add_unassigned_test_users("courses.db")
