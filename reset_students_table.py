import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute('''
    CREATE TABLE students (
        id TEXT PRIMARY KEY,
        username TEXT,
        email TEXT,
        role TEXT,
        join_date TEXT,
        attendance INTEGER,
        exam_status TEXT,
        exam_score INTEGER,
        a1_score INTEGER,
        a1_status TEXT,
        a1_penalty TEXT,
        a2_score INTEGER,
        a2_status TEXT,
        a2_penalty TEXT,
        status TEXT,
        enrollment_status TEXT
    )
''')

conn.commit()
conn.close()
print("✅ Students table reset successfully.")
