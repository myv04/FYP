import sqlite3

def fetch_student_dashboard():
    conn = sqlite3.connect("reports_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT student_name, student_id, average_attendance FROM student_profile LIMIT 1")
    student = cursor.fetchone()

    cursor.execute("SELECT module_name, grade FROM student_grades")
    grades = cursor.fetchall()

    cursor.execute("SELECT module_name, assignment_name, score, status FROM student_assignments")
    assignments = cursor.fetchall()

    cursor.execute("SELECT module_name, exam_name, score, status FROM student_exams")
    exams = cursor.fetchall()

    cursor.execute("SELECT module_name, assignment_name, deadline_date, days_left FROM student_deadlines")
    deadlines = cursor.fetchall()

    conn.close()

    return {
        "student_name": student[0],
        "student_id": student[1],
        "attendance": student[2],
        "grades": grades,
        "assignments": assignments,
        "exams": exams,
        "deadlines": deadlines
    }
