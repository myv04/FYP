import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Connect to your new database
conn = sqlite3.connect('course_members.db')
c = conn.cursor()

# Create the table
c.execute('''
CREATE TABLE IF NOT EXISTS course_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id TEXT UNIQUE,
    name TEXT,
    role TEXT,
    course TEXT,
    join_date TEXT
)
''')

# Initialize Faker
fake = Faker()

# Define roles
roles = ["Student", "Lecturer", "Admin", "Teaching Assistant"]

# Define courses
courses = ["Data Science", "Software Engineering"]

# Helper function to generate random date
def random_date(start_days_ago=365, end_days_ago=1):
    days_ago = random.randint(end_days_ago, start_days_ago)
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d")

# Generate members
members = []

# Students (total: 950 — 500 SE + 450 DS)
for _ in range(500):
    members.append(("SE" + str(random.randint(1000, 9999)), fake.name(), "Student", "Software Engineering", random_date()))

for _ in range(450):
    members.append(("DS" + str(random.randint(1000, 9999)), fake.name(), "Student", "Data Science", random_date()))

# Lecturers (total: ~30 SE + ~25 DS)
for _ in range(30):
    members.append(("SE" + str(random.randint(1000, 9999)), fake.name(), "Lecturer", "Software Engineering", random_date()))
for _ in range(25):
    members.append(("DS" + str(random.randint(1000, 9999)), fake.name(), "Lecturer", "Data Science", random_date()))

# Admins (let’s say 5 per course)
for _ in range(5):
    members.append(("SE" + str(random.randint(1000, 9999)), fake.name(), "Admin", "Software Engineering", random_date()))
for _ in range(5):
    members.append(("DS" + str(random.randint(1000, 9999)), fake.name(), "Admin", "Data Science", random_date()))

# Teaching Assistants (10 each course)
for _ in range(10):
    members.append(("SE" + str(random.randint(1000, 9999)), fake.name(), "Teaching Assistant", "Software Engineering", random_date()))
for _ in range(10):
    members.append(("DS" + str(random.randint(1000, 9999)), fake.name(), "Teaching Assistant", "Data Science", random_date()))

# Remove potential duplicates by checking member_id
unique_members = {}
for member in members:
    if member[0] not in unique_members:
        unique_members[member[0]] = member

# Insert members into the database
c.executemany('''
INSERT INTO course_members (member_id, name, role, course, join_date)
VALUES (?, ?, ?, ?, ?)
''', list(unique_members.values()))

# Commit and close
conn.commit()
conn.close()

print("✅ Course members data populated successfully!")
