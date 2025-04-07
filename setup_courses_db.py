import sqlite3

# Connect to courses.db
conn = sqlite3.connect('courses.db')
c = conn.cursor()

# Drop existing tables
c.execute('DROP TABLE IF EXISTS enrollments')
c.execute('DROP TABLE IF EXISTS students')
c.execute('DROP TABLE IF EXISTS courses')

# Create Courses table
c.execute('''
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    students INTEGER DEFAULT 0,
    lecturers INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Active',
    attendance INTEGER DEFAULT 75,
    average_grade REAL DEFAULT 65,
    satisfaction INTEGER DEFAULT 4
)
''')

# Create Students table
c.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uni_id TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT CHECK(role IN ('Student', 'Lecturer', 'Admin', 'Teacher Assistant')) NOT NULL DEFAULT 'Student',
    join_date TEXT,
    enrollment_status TEXT DEFAULT 'Active'
)
''')

# Create Enrollments table
c.execute('''
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
''')

conn.commit()
conn.close()

print("✅ Database and tables created successfully.")
