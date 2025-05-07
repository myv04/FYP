# populate_ws201_students_safe.py
import sqlite3
import random

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Step 1: Get 50 original SE101 dashboard students
original_dashboard_ids = [
    'SE8946', 'SE5918', 'SE7494', 'SE1509', 'SE8253', 'SE1744', 'SE5043', 'SE8979', 'SE1968', 'SE1852',
    'SE8330', 'SE8811', 'SE9771', 'SE5353', 'SE1179', 'SE5838', 'SE4247', 'SE4796', 'SE3642', 'SE3570',
    'SE3688', 'SE9940', 'SE5462', 'SE4267', 'SE2196', 'SE3056', 'SE3902', 'SE5236', 'SE9158', 'SE8950',
    'SE1967', 'SE8256', 'SE4532', 'SE1517', 'SE7469', 'SE8148', 'SE1419', 'SE6287', 'SE3159', 'SE3655',
    'SE9723', 'SE9035', 'SE9083', 'SE2110', 'SE6193', 'SE4227', 'SE1890', 'SE1314', 'SE5890', 'SE3935'
]

# Step 2: Find SE101 students with 'student' role (case/space insensitive) not in dashboards
cursor.execute(f"""
    SELECT s.id
    FROM students s
    JOIN enrollments e ON s.id = e.student_id
    WHERE 
        e.course_id = 'SE101'
        AND LOWER(TRIM(s.role)) = 'student'
        AND s.id NOT IN ({','.join(['?'] * len(original_dashboard_ids))})
    LIMIT 80
""", original_dashboard_ids)

candidates = [row[0] for row in cursor.fetchall()]

# Step 3: Enroll into WS201 and update assignment fields
for student_id in candidates:
    cursor.execute("INSERT OR IGNORE INTO module_enrollments (student_id, module_code) VALUES (?, ?)", (student_id, 'WS201'))

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
print(f"✅ Enrolled {len(candidates)} SE101 students into WS201 with dashboard-ready data.")
