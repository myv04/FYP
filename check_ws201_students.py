import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*) FROM students s
JOIN module_enrollments me ON s.id = me.student_id
WHERE me.module_code = 'WS201' AND LOWER(s.role) = 'student'
""")

count = cursor.fetchone()[0]
print(f"✅ WS201 student records found: {count}")

conn.close()
