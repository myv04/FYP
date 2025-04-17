import sqlite3

conn = sqlite3.connect("reports_data.db")
cursor = conn.cursor()

# 👤 Student profile
cursor.execute("INSERT INTO student_profile (student_name, student_id, average_attendance) VALUES (?, ?, ?)", 
               ("Mohammed Vohra", "210034354", "65%"))

# 🎓 Grades
grades = [
    ("CS201", "Data Structure & Algorithm", 70),
    ("CS202", "Web Development", 73),
    ("CS203", "Artificial Intelligence", 25.5),
    ("CS204", "Database Management", 36),
    ("CS205", "Cybersecurity", 68.8)
]
cursor.executemany("INSERT INTO student_grades (module_code, module_name, grade) VALUES (?, ?, ?)", grades)

# 📝 Assignments
assignments = [
    ("CS202", "Web Development", "Responsive Design Project", "82%", "Completed"),
    ("CS203", "Artificial Intelligence", "Neural Network Implementation", "85%", "Completed"),
    ("CS203", "Artificial Intelligence", "Ethical Concerns in AI Development", "n/a", "Not Completed"),
    ("CS203", "Artificial Intelligence", "Sentiment Analysis using NLP", "n/a", "Not Started"),
    ("CS204", "Database Management", "Normalization Techniques", "88%", "Completed"),
    ("CS204", "Database Management", "SQL Query Optimization", "92%", "Completed"),
    ("CS205", "Cybersecurity", "Network Security Protocols", "80%", "Completed"),
    ("CS205", "Cybersecurity", "Ethical Hacking Fundamentals", "68%", "Completed"),
    ("CS205", "Cybersecurity", "Malware Analysis", "n/a", "Not Started"),
]
cursor.executemany("INSERT INTO student_assignments (module_code, module_name, assignment_name, score, status) VALUES (?, ?, ?, ?, ?)", assignments)

# 🧪 Exams
exams = [
    ("CS201", "Data Structure & Algorithm", "DSA Exam", "78%", "Completed"),
    ("CS202", "Web Development", "Web Dev Exam", "85%", "Completed"),
    ("CS204", "Database Management", "Ethical Concerns in AI Development", "n/a", "Not Completed")
]
cursor.executemany("INSERT INTO student_exams (module_code, module_name, exam_name, score, status) VALUES (?, ?, ?, ?, ?)", exams)

# 📅 Deadlines
deadlines = [
    ("CS203", "Artificial Intelligence", "Ethical Concerns in AI Development", "21/03/2025", "10"),
    ("CS202", "Web Development", "Sentiment Analysis using NLP", "TBC", "TBC"),
    ("CS204", "Database Management", "Malware Analysis", "TBC", "TBC")
]
cursor.executemany("INSERT INTO student_deadlines (module_code, module_name, assignment_name, deadline_date, days_left) VALUES (?, ?, ?, ?, ?)", deadlines)

# 📊 Attendance overview
attendance = [
    ("Data Structures", 75),
    ("Web Development", 80),
    ("AI", 85),
    ("Databases", 70),
    ("Cybersecurity", 65)
]
cursor.executemany("INSERT INTO attendance_overview (module_name, avg_attendance) VALUES (?, ?)", attendance)

conn.commit()
conn.close()
print("✅ Student data seeded.")
