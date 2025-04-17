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

# 🔐 Original Cybersecurity Dashboard Data
save_module_data(
    module_code="CS205",
    module_name="Cybersecurity",
    attendance=88,
    grade=68.8,  # Based on two completed assignments
    assignments=[
        {"name": "Network Security Protocols", "status": "Completed", "score": 95},
        {"name": "Ethical Hacking Fundamentals", "status": "Completed", "score": 88},
        {"name": "Malware Analysis", "status": "Not Started"}
    ],
    exams=[],
    deadlines=[
        {"name": "Malware Analysis", "deadline": "TBC", "days_left": "TBC"}
    ]
)

print("✅ CS205 Cybersecurity data inserted successfully.")
