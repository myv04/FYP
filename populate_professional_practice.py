import sqlite3
import random

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# ✅ Students already used in other dashboards (adjust if needed)
used_ids = [
    # 50 SE101 students already in dashboards
    'SE8946', 'SE5918', 'SE7494', 'SE1509', 'SE8253', 'SE1744', 'SE5043', 'SE8979', 'SE1968', 'SE1852',
    'SE8330', 'SE8811', 'SE9771', 'SE5353', 'SE1179', 'SE5838', 'SE4247', 'SE4796', 'SE3642', 'SE3570',
    'SE3688', 'SE9940', 'SE5462', 'SE4267', 'SE2196', 'SE3056', 'SE3902', 'SE5236', 'SE9158', 'SE8950',
    'SE1967', 'SE8256', 'SE4532', 'SE1517', 'SE7469', 'SE8148', 'SE1419', 'SE6287', 'SE3159', 'SE3655',
    'SE9723', 'SE9035', 'SE9083', 'SE2110', 'SE6193', 'SE4227', 'SE1890', 'SE1314', 'SE5890', 'SE3935',
    
    # 80 DS102 students from Big Data dashboard (if known, add here)
]

# ✅ Select 40 SE101 students not used elsewhere
cursor.execute(f"""
    SELECT s.id FROM students s
    JOIN enrollments e ON s.id = e.student_id
    WHERE e.course_id = 'SE101' AND LOWER(TRIM(s.role)) = 'student' AND s.id NOT IN ({','.join(['?'] * len(used_ids))})
    LIMIT 40
""", used_ids)
se_students = [row[0] for row in cursor.fetchall()]

# ✅ Select 40 DS101 students not used elsewhere
cursor.execute(f"""
    SELECT s.id FROM students s
    JOIN enrollments e ON s.id = e.student_id
    WHERE e.course_id = 'DS101' AND LOWER(TRIM(s.role)) = 'student' AND s.id NOT IN ({','.join(['?'] * len(used_ids))})
    LIMIT 40
""", used_ids)
ds_students = [row[0] for row in cursor.fetchall()]

# ✅ Combine and enroll
combined_ids = se_students + ds_students

for student_id in combined_ids:
    cursor.execute("INSERT OR IGNORE INTO module_enrollments (student_id, module_code) VALUES (?, ?)", (student_id, 'CSDS101'))

    # Add assignment and attendance data
    cursor.execute("""
        UPDATE students
        SET attendance = ?,
            a1_score = ?,
            a1_status = 'Completed',
            a1_penalty = 'None',
            status = 'Enrolled'
        WHERE id = ?
    """, (
        random.randint(70, 100),
        round(random.uniform(65, 95), 2),
        student_id
    ))

conn.commit()
conn.close()
print(f"✅ Enrolled {len(combined_ids)} students into CSDS101 with full dashboard data.")
