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

# ✅ Save the ORIGINAL data from your dashboard
save_module_data(
    module_code="CS204",
    module_name="Database Management",
    attendance=82,
    grade=36.0,  # Weighted grade from assignments only
    assignments=[
        {"name": "Normalization Techniques", "status": "Completed", "score": 88},
        {"name": "SQL Query Optimization", "status": "Completed", "score": 92}
    ],
    exams=[
        {"name": "Final Database Exam", "status": "Not Completed"}  # No score yet
    ],
    deadlines=[
        {"name": "Final Database Exam", "deadline": "TBC", "days_left": "TBC"}
    ]
)

print("✅ CS204 data inserted into student_performance.db")
