import sqlite3

def insert_course(name="Software Engineering", code="SE101"):
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    # Check if course already exists
    course = cursor.execute("SELECT * FROM courses WHERE name = ?", (name,)).fetchone()
    if course:
        print(f"ℹ️ Course '{name}' already exists (ID: {course[0]})")
        return

    cursor.execute("""
        INSERT INTO courses (name, code, students, lecturers, status)
        VALUES (?, ?, ?, ?, ?)
    """, (name, code, "", "", "Active"))

    conn.commit()
    print(f"✅ Course '{name}' inserted successfully.")
    conn.close()

if __name__ == "__main__":
    insert_course()
