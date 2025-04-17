import sqlite3

# Connect to the new database file (this will create it if it doesn't exist)
conn = sqlite3.connect("student_performance.db")

# Create a table for module data
conn.execute('''
    CREATE TABLE IF NOT EXISTS student_modules (
        module_code TEXT PRIMARY KEY,
        module_name TEXT,
        attendance REAL,
        grade REAL,
        assignments_json TEXT,
        exams_json TEXT,
        deadlines_json TEXT
    )
''')

conn.commit()
conn.close()

print("✅ Database and table created: student_performance.db")
