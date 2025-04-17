import sqlite3
import json

def save_module_data(module_code, module_name, attendance, grade, assignments, exams, deadlines):
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()

    assignments_json = json.dumps(assignments)
    exams_json = json.dumps(exams)
    deadlines_json = json.dumps(deadlines)

    c.execute('''
        INSERT OR REPLACE INTO student_modules
        (module_code, module_name, attendance, grade, assignments_json, exams_json, deadlines_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (module_code, module_name, attendance, grade, assignments_json, exams_json, deadlines_json))

    conn.commit()
    conn.close()

# 🔹 Replace with your actual data from the current dashboard
save_module_data(
    module_code="CS201",
    module_name="Data Structures & Algorithms",
    attendance=75,
    grade=78,  # Based on your dashboard
    assignments=[],
    exams=[
        {"name": "DSA Exam", "status": "Completed", "score": 78}
    ],
    deadlines=[]
)

print("✅ CS201 data inserted.")
