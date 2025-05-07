import sqlite3
import random

def seed_data():
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    # Drop and recreate table
    cursor.execute('DROP TABLE IF EXISTS dashboard_professional_practice')
    cursor.execute('''
    CREATE TABLE dashboard_professional_practice (
        id TEXT PRIMARY KEY,
        name TEXT,
        course TEXT,
        a1_score INTEGER,
        a2_score INTEGER,
        attendance INTEGER
    )
    ''')

    # Fetch students by course & role
    ds_students = cursor.execute('''
        SELECT s.id, s.username FROM students s
        JOIN enrollments e ON s.id = e.student_id
        JOIN courses c ON e.course_id = c.id
        WHERE c.name LIKE '%Data Science%' AND c.year = 2025 AND s.role = 'Student'
    ''').fetchall()

    se_students = cursor.execute('''
        SELECT s.id, s.username FROM students s
        JOIN enrollments e ON s.id = e.student_id
        JOIN courses c ON e.course_id = c.id
        WHERE c.name LIKE '%Software Engineering%' AND c.year = 2025 AND s.role = 'Student'
    ''').fetchall()

    # Create name-to-data maps
    ds_map = {name: (id_, name) for id_, name in ds_students}
    se_map = {name: (id_, name) for id_, name in se_students}

    # Remove overlapping names
    common_names = set(ds_map.keys()) & set(se_map.keys())
    for name in common_names:
        ds_map.pop(name, None)
        se_map.pop(name, None)

    # Sample 25 unique names per course
    ds_sample = random.sample(list(ds_map.values()), min(25, len(ds_map)))
    se_sample = random.sample(list(se_map.values()), min(25, len(se_map)))

    all_students = [(s[0], s[1], "Data Science") for s in ds_sample] + \
                   [(s[0], s[1], "Software Engineering") for s in se_sample]

    for student_id, name, course in all_students:
        a1 = random.randint(60, 95)
        a2 = random.randint(55, 90)
        attendance = random.randint(70, 100)
        cursor.execute('''
            INSERT OR REPLACE INTO dashboard_professional_practice (id, name, course, a1_score, a2_score, attendance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, name, course, a1, a2, attendance))

    conn.commit()
    conn.close()
    print(f"✅ Seeded {len(ds_sample)} DS + {len(se_sample)} SE students with unique names.")

if __name__ == "__main__":
    seed_data()
