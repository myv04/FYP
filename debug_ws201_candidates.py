# debug_ws201_candidates.py
import sqlite3

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

original_dashboard_ids = [
    'SE8946', 'SE5918', 'SE7494', 'SE1509', 'SE8253', 'SE1744', 'SE5043', 'SE8979', 'SE1968', 'SE1852',
    'SE8330', 'SE8811', 'SE9771', 'SE5353', 'SE1179', 'SE5838', 'SE4247', 'SE4796', 'SE3642', 'SE3570',
    'SE3688', 'SE9940', 'SE5462', 'SE4267', 'SE2196', 'SE3056', 'SE3902', 'SE5236', 'SE9158', 'SE8950',
    'SE1967', 'SE8256', 'SE4532', 'SE1517', 'SE7469', 'SE8148', 'SE1419', 'SE6287', 'SE3159', 'SE3655',
    'SE9723', 'SE9035', 'SE9083', 'SE2110', 'SE6193', 'SE4227', 'SE1890', 'SE1314', 'SE5890', 'SE3935'
]

query = """
    SELECT s.id, s.username, s.role
    FROM students s
    JOIN enrollments e ON s.id = e.student_id
    WHERE e.course_id = 'SE101' AND LOWER(s.role) = 'student' AND s.id NOT IN ({})
""".format(','.join(['?'] * len(original_dashboard_ids)))

cursor.execute(query, original_dashboard_ids)
rows = cursor.fetchall()

print(f"✅ Eligible SE101 students (excluding 50 used already): {len(rows)}\n")
for row in rows[:10]:
    print(row)

conn.close()
