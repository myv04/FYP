import sqlite3

conn = sqlite3.connect("reports_data.db")
cursor = conn.cursor()

# 🧑 Student Dashboard Overview
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    average_attendance TEXT
)
''')

# 🎓 Grades per module
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_code TEXT,
    module_name TEXT,
    grade REAL
)
''')

# 📝 Assignment records
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_code TEXT,
    module_name TEXT,
    assignment_name TEXT,
    score TEXT,
    status TEXT
)
''')

# 🧪 Exams
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_code TEXT,
    module_name TEXT,
    exam_name TEXT,
    score TEXT,
    status TEXT
)
''')

# 📅 Deadlines
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_deadlines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_code TEXT,
    module_name TEXT,
    assignment_name TEXT,
    deadline_date TEXT,
    days_left TEXT
)
''')

# 📊 Attendance Summary (for separate Attendance Report)
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance_overview (
    module_name TEXT,
    avg_attendance INTEGER
)
''')

conn.commit()
conn.close()
print("✅ Student and attendance tables created.")
