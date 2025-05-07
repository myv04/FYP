# remove_protected_from_ds102.py
import sqlite3

# Load the 50 protected student IDs
with open("protected_ids.txt", "r") as f:
    protected_ids = [line.strip() for line in f.readlines()]

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Remove protected students from DS102
cursor.execute(f"""
    DELETE FROM module_enrollments
    WHERE module_code = 'DS102' AND student_id IN ({','.join(['?']*len(protected_ids))})
""", protected_ids)

conn.commit()
conn.close()

print(f"✅ Removed {len(protected_ids)} protected students from DS102.")
