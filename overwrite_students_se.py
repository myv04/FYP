import sqlite3
from datetime import datetime
from course_data import software_engineering_students

def clear_existing_students(course_id):
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    # Get IDs of current non-staff students enrolled in this course
    student_ids = cursor.execute('''
        SELECT s.id FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = ? AND s.role = "Student"
    ''', (course_id,)).fetchall()

    # Delete only students, not staff
    for (sid,) in student_ids:
        cursor.execute("DELETE FROM enrollments WHERE student_id = ?", (sid,))
        cursor.execute("DELETE FROM students WHERE id = ?", (sid,))

    conn.commit()
    conn.close()
    print(f"🧹 Cleared {len(student_ids)} existing students from course ID {course_id}.\n")


def insert_original_students(course_id):
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    print(f"📦 Inserting original 50 students into course ID {course_id}...\n")

    for student in software_engineering_students:
        name = student["name"]
        uni_id = f"SE{str(student['id']).zfill(5)}"
        email = f"{name.replace(' ', '').lower()}@uni.com"
        role = "Student"
        join_date = datetime.now().strftime("%Y-%m-%d")
        enrollment_status = "Active"

        # Insert into students table
        cursor.execute("""
            INSERT INTO students (
                uni_id, username, email, role, join_date, enrollment_status,
                attendance, exam_status, exam_score,
                a1_score, a1_status, a1_penalty,
                a2_score, a2_status, a2_penalty,
                status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uni_id, name, email, role, join_date, enrollment_status,
            student["attendance"], student["exam_status"], student["exam_score"],
            student["a1_score"], student["a1_status"], student["a1_penalty"],
            student["a2_score"], student["a2_status"], student["a2_penalty"],
            student["status"]
        ))

        student_id = cursor.lastrowid

        # Link to course
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))

        print(f"✅ Inserted: {name}")

    conn.commit()
    conn.close()
    print("\n🎉 All 50 students added successfully.\n")


def run_seeding():
    course_id = 3  # Software Engineering
    clear_existing_students(course_id)
    insert_original_students(course_id)

if __name__ == "__main__":
    run_seeding()
