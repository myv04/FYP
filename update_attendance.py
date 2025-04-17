import sqlite3

# Correct attendance values
updates = {
    "CS201": 75,  # Data Structures
    "CS202": 80,  # Web Dev
    "CS203": 70,  # AI
    "CS204": 85,  # DB
    "CS205": 78   # Cyber
}

conn = sqlite3.connect("reports_data.db")
cursor = conn.cursor()

for module_code, attendance in updates.items():
    cursor.execute("""
        UPDATE report_data SET avg_attendance = ?
        WHERE module_code = ?
    """, (attendance, module_code))

conn.commit()
conn.close()

print("✅ Attendance values successfully updated.")
