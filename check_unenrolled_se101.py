# check_unenrolled_se101.py
import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Get SE101 students not in module_enrollments
cursor.execute("""
    SELECT s.id, s.username
    FROM students s
    JOIN enrollments e ON s.id = e.student_id
    WHERE e.course_id = 'SE101'
      AND s.role = 'Student'
      AND s.id NOT IN (
          SELECT student_id FROM module_enrollments
      )
    LIMIT 100
""")

results = cursor.fetchall()
conn.close()

print(f"Found {len(results)} SE101 students NOT linked to any module.")
for sid, name in results:
    print(f"- {sid}: {name}")
