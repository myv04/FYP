import sqlite3

conn = sqlite3.connect("reports_data.db")
cursor = conn.cursor()

# --- Insert sample modules
modules = [
    ("CS201", "Data Structure & Algorithm"),
    ("CS202", "Web Development"),
    ("CS203", "Artificial Intelligence"),
    ("CS204", "Database Management"),
    ("CS205", "Cybersecurity")
]
cursor.executemany("INSERT INTO modules (module_code, module_name) VALUES (?, ?)", modules)

# --- Insert sample report data
report_data = [
    ("CS201", 85, 1, 0, 78),
    ("CS202", 80, 1, 0, 79),
    ("CS203", 75, 1, 2, 25.5),
    ("CS204", 82, 2, 1, 36),
    ("CS205", 78, 2, 1, 68.8)
]
cursor.executemany("""
    INSERT INTO report_data (module_code, avg_attendance, assignments_completed, assignments_pending, current_grade)
    VALUES (?, ?, ?, ?, ?)""", report_data)

# --- Insert assessments
assessments = [
    ("CS201", "DSA Exam", 78),
    ("CS202", "Final Web Development Exam", 76),
    ("CS202", "Responsive Design Project", 82),
    ("CS203", "Neural Network Implementation", 85),
    ("CS203", "Ethical Concerns in AI Development", None),
    ("CS203", "Sentiment Analysis using NLP", None),
    ("CS204", "Normalization Techniques", 88),
    ("CS204", "SQL Query Optimization", 92),
    ("CS204", "Final Database Exam", None),
    ("CS205", "Network Security Protocols", 95),
    ("CS205", "Ethical Hacking Fundamentals", 88),
    ("CS205", "Malware Analysis", None)
]
cursor.executemany("INSERT INTO assessments (module_code, assessment_name, score) VALUES (?, ?, ?)", assessments)

conn.commit()
conn.close()

print("✅ reports_data.db seeded with sample data.")
