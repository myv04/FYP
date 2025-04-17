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

# 📊 Use the same values you were using in your current dashboard
save_module_data(
    module_code="CS203",
    module_name="Artificial Intelligence",
    attendance=68,
    grade=25.5,
    assignments=[
        {"name": "Neural Network Implementation", "status": "Completed", "score": 85},
        {"name": "Ethical Concerns in AI Development", "status": "Not Completed"},
        {"name": "Sentiment Analysis using NLP", "status": "Not Started"}
    ],
    exams=[],
    deadlines=[
        {"name": "Ethical Concerns in AI Development", "deadline": "21/03/2025", "days_left": "10"},
        {"name": "Sentiment Analysis using NLP", "deadline": "TBC", "days_left": "TBC"}
    ]
)

print("✅ CS203 data inserted.")
