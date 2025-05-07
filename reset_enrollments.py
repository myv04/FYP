import sqlite3

def clear_enrollments(course_id):
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrollments WHERE course_id = ?", (course_id,))
    conn.commit()
    conn.close()
    print(f"🧹 Cleared enrollments for course {course_id}")

def run():
    clear_enrollments(3)  # Software Engineering
    clear_enrollments(4)  # Data Science

if __name__ == "__main__":
    run()
