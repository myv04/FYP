import sqlite3
from datetime import datetime
from course_data import software_engineering_students, data_science_students

def sync_students(students, course_id):
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    inserted = 0
    linked = 0
    updated = 0

    for student in students:
        name = student["name"]
        role = "Student"
        join_date = datetime.now().strftime("%Y-%m-%d")
        email = f"{name.replace(' ', '').lower()}@uni.com"
        enrollment_status = "Active"

        # Check if student already exists by username
        cursor.execute("SELECT id FROM students WHERE username = ?", (name,))
        existing = cursor.fetchone()

        if existing:
            student_id = existing[0]
            updated += 1
        else:
            # Insert new student
            cursor.execute("""
                INSERT INTO students (
                    username, email, role, join_date, enrollment_status,
                    attendance, exam_status, exam_score,
                    a1_score, a1_status, a1_penalty,
                    a2_score, a2_status, a2_penalty,
                    status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, email, role, join_date, enrollment_status,
                student["attendance"], student["exam_status"], student["exam_score"],
                student["a1_score"], student["a1_status"], student["a1_penalty"],
                student["a2_score"], student["a2_status"], student["a2_penalty"],
                student["status"]
            ))
            student_id = cursor.lastrowid
            inserted += 1

        # Link student to course if not already enrolled
        cursor.execute("""
            SELECT 1 FROM enrollments WHERE student_id = ? AND course_id = ?
        """, (student_id, course_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO enrollments (student_id, course_id)
                VALUES (?, ?)
            """, (student_id, course_id))
            linked += 1

    conn.commit()
    conn.close()

    print(f"✅ Inserted: {inserted}")
    print(f"🔁 Linked:   {linked}")
    print(f"🛠️  Updated: {updated}")


def run():
    print("\n📘 Syncing Software Engineering students...")
    sync_students(software_engineering_students, course_id=3)

    print("\n📗 Syncing Data Science students...")
    sync_students(data_science_students, course_id=4)


if __name__ == "__main__":
    run()
