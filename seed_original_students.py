import sqlite3
from datetime import datetime
from course_data import software_engineering_students  # Make sure this file is in your project folder

def seed_exact_students(course_id=3):  # Use the correct ID for BSc Software Engineering
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    course = cursor.execute("SELECT name FROM courses WHERE id = ?", (course_id,)).fetchone()
    if not course:
        print(f"❌ Course with ID {course_id} not found.")
        return

    print(f"\n✅ Seeding original students into course: {course[0]}\n")

    for student in software_engineering_students:
        # Create fake but consistent info from student data
        name = student["name"]
        uni_id = f"SE{str(student['id']).zfill(5)}"
        email = f"{name.replace(' ', '').lower()}@uni.com"
        role = "Student"
        join_date = datetime.now().strftime("%Y-%m-%d")
        enrollment_status = "Active"

        # Check if student already exists to avoid duplicates
        exists = cursor.execute("SELECT * FROM students WHERE username = ? AND email = ?", (name, email)).fetchone()
        if exists:
            print(f"⏭️ Skipping {name} (already exists)")
            continue

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

        # Link student to course
        cursor.execute("""
            INSERT INTO enrollments (student_id, course_id)
            VALUES (?, ?)
        """, (student_id, course_id))

        print(f"✅ Added: {name}")

    conn.commit()
    conn.close()
    print("\n🎉 All done! Students have been seeded into the DB.\n")

if __name__ == "__main__":
    seed_exact_students(course_id=3)
