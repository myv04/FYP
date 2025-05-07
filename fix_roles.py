# fix_roles.py
import sqlite3

# Connect to your database
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Update all roles to lowercase and remove extra spaces
cursor.execute("""
    UPDATE students
    SET role = TRIM(LOWER(role))
""")

conn.commit()
conn.close()
print("✅ Roles cleaned (lowercased + trimmed).")
