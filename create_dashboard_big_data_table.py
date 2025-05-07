import sqlite3

conn = sqlite3.connect("instance/database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS dashboard_big_data (
    id TEXT PRIMARY KEY,
    student TEXT,
    "Final Grade" REAL,
    "Attendance (%)" REAL,
    "Assignment 1 (Data Lakes)" REAL,
    "Assignment 1 Status" TEXT,
    "Assignment 1 Penalty" TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("✅ Created table: dashboard_big_data")
