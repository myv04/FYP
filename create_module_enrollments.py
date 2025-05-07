import sqlite3

# Connect to your database
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Create the module_enrollments table
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
