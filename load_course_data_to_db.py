from course_data import software_engineering_students, data_science_students
import sqlite3

def insert_students(course_name, students_list):
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    # Get course_id from course name
    course = cursor.execute('SELECT id FROM courses WHERE name LIKE ?', (f'%{course_name}%',)).fetchone()
    if not course:
        print(f"Course '{course_name}' not found in DB!")
        return
    course_id = course[0]

    for s in students_list:
        cursor.execute('''
            INSERT INTO students (uni_id, username, email, role, join_date, enrollment_status)
            VALUES (?, ?, ?, ?, date('now'), ?)
        ''', (s["id"], s["name"], f"{s['name'].replace(' ', '').lower()}@uni.com", "Student", "Active"))
        student_id = cursor.lastrowid
        cursor.execute('INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)', (student_id, course_id))

    conn.commit()
    conn.close()
    print(f"Inserted {len(students_list)} students into '{course_name}'.")

insert_students("Software Engineering", software_engineering_students)
insert_students("Data Science", data_science_students)
