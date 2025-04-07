import sqlite3
from faker import Faker
from datetime import datetime
import random

fake = Faker()

# Helpers
def generate_student_uni_id(prefix):
    return f"{prefix}{random.randint(100000, 999999)}"

def generate_staff_uni_id(existing_ids):
    while True:
        number = random.randint(100000, 999999)
        if number not in existing_ids:
            existing_ids.add(number)
            return str(number)

def generate_student_email(name, uni_id):
    initials = ''.join([n[0].upper() for n in name.split() if n])
    return f"{initials}{uni_id}@uni.com"

def generate_staff_email(name):
    return f"{name.replace(' ', '')}@uni.com"

# Connect to DB
conn = sqlite3.connect('courses.db')
c = conn.cursor()

# Step 1: Clean tables
c.execute('DELETE FROM enrollments')
c.execute('DELETE FROM students')
c.execute('DELETE FROM courses')
conn.commit()

# Step 2: Add courses
courses = [
    ('BSc Software Engineering', 'SE101'),
    ('BSc Data Science', 'DS102')
]
c.executemany('INSERT INTO courses (name, code) VALUES (?, ?)', courses)
conn.commit()

# Step 3: Prepare data
c.execute('SELECT id, code FROM courses')
course_map = {code: id for (id, code) in c.fetchall()}

students = []
enrollments = []
existing_staff_ids = set()

# Settings
course_settings = {
    'SE101': {'prefix': 'SE', 'students': 500, 'lecturers': 30, 'admins': 5, 'tas': 10},
    'DS102': {'prefix': 'DS', 'students': 450, 'lecturers': 25, 'admins': 5, 'tas': 10}
}

join_date = datetime.now().strftime('%Y-%m-%d')
enrollment_status = 'Active'

for course_code, settings in course_settings.items():
    prefix = settings['prefix']
    course_id = course_map[course_code]

    # 1. Students
    for _ in range(settings['students']):
        name = fake.name()
        uni_id = generate_student_uni_id(prefix)
        email = generate_student_email(name, uni_id)
        students.append((uni_id, name, email, 'Student', join_date, enrollment_status))
    
    # 2. Lecturers
    for _ in range(settings['lecturers']):
        name = fake.name()
        uni_id = generate_staff_uni_id(existing_staff_ids)
        email = generate_staff_email(name)
        students.append((uni_id, name, email, 'Lecturer', join_date, enrollment_status))
    
    # 3. Admins
    for _ in range(settings['admins']):
        name = fake.name()
        uni_id = generate_staff_uni_id(existing_staff_ids)
        email = generate_staff_email(name)
        students.append((uni_id, name, email, 'Admin', join_date, enrollment_status))
    
    # 4. Teacher Assistants
    for _ in range(settings['tas']):
        name = fake.name()
        uni_id = generate_staff_uni_id(existing_staff_ids)
        email = generate_staff_email(name)
        students.append((uni_id, name, email, 'Teacher Assistant', join_date, enrollment_status))

# Step 4: Insert students
c.executemany('''
INSERT INTO students (uni_id, username, email, role, join_date, enrollment_status)
VALUES (?, ?, ?, ?, ?, ?)
''', students)
conn.commit()

# Step 5: Prepare enrollments
c.execute('SELECT id, uni_id FROM students')
students_in_db = c.fetchall()

for student_id, uni_id in students_in_db:
    if uni_id.startswith('SE'):
        course_id = course_map['SE101']
    elif uni_id.startswith('DS'):
        course_id = course_map['DS102']
    else:
        # Assign staff members to both courses for visibility
        for cid in course_map.values():
            enrollments.append((student_id, cid))
        continue

    enrollments.append((student_id, course_id))

# Step 6: Insert enrollments
c.executemany('''
INSERT INTO enrollments (student_id, course_id)
VALUES (?, ?)
''', enrollments)
conn.commit()

# Step 7: Update course counts dynamically
for course_code, settings in course_settings.items():
    course_id = course_map[course_code]
    student_count = settings['students']
    lecturer_count = settings['lecturers']
    c.execute("UPDATE courses SET students = ?, lecturers = ? WHERE id = ?", (student_count, lecturer_count, course_id))

conn.commit()
conn.close()

print("✅ Data seeded successfully with perfect format for UNI ID and emails!")
