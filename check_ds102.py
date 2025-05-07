import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Check total enrollments in DS102
cursor.execute("SELECT COUNT(*) FROM module_enrollments WHERE module_code = 'DS102'")
print("DS102 total enrollments:", cursor.fetchone()[0])

# Check how many students are linked to DS102 and have the correct role
cursor.execute("""
    SELECT COUNT(*) FROM students
    WHERE LOWER(role) = 'student'
    AND id IN (
        SELECT student_id FROM module_enrollments WHERE module_code = 'DS102'
    )
""")
print("DS102 students with correct role:", cursor.fetchone()[0])
