# create_module_enrollments_table.py
import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS module_enrollments (
    student_id TEXT,
    module_code TEXT,
    UNIQUE(student_id, module_code)
)
""")

conn.commit()
conn.close()

print("✅ module_enrollments table created.")
