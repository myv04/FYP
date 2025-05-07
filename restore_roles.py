# restore_roles.py
import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Set the role back to "Student" or "Lecturer" as originally stored
cursor.execute("""
    UPDATE students
    SET role = 
        CASE 
            WHEN role = 'student' THEN 'Student'
            WHEN role = 'lecturer' THEN 'Lecturer'
            ELSE role
        END
""")

conn.commit()
conn.close()
print("✅ Roles restored to original capitalization (Student/Lecturer).")
