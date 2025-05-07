import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Clear existing DS102 enrollments first
cursor.execute("DELETE FROM module_enrollments WHERE module_code = 'DS102'")

# Get 80 valid students
students = cursor.execute("""
    SELECT id FROM students
    WHERE id LIKE 'DS%' AND LOWER(role) = 'student'
      AND a1_score IS NOT NULL
      AND a1_status IS NOT NULL
      AND a1_penalty IS NOT NULL
      AND attendance IS NOT NULL
      AND status IS NOT NULL
    LIMIT 80
""").fetchall()

print(f"Found {len(students)} eligible DS students. Linking to DS102...")

for (student_id,) in students:
    cursor.execute("""
        INSERT OR IGNORE INTO module_enrollments (student_id, module_code)
        VALUES (?, ?)
    """, (student_id, "DS102"))

conn.commit()
conn.close()
print("✅ DS102 module enrollments updated.")
