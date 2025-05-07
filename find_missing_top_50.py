import sqlite3
from course_data import software_engineering_students, data_science_students

def find_missing_students():
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    all_students = software_engineering_students + data_science_students

    missing = []

    for student in all_students:
        name = student["name"]
        cursor.execute("SELECT id FROM students WHERE username = ?", (name,))
        if not cursor.fetchone():
            missing.append(name)

    conn.close()

    print("🔍 Missing students from DB:")
    for name in missing:
        print(f"❌ {name}")

    print(f"\nTotal missing: {len(missing)}")

if __name__ == "__main__":
    find_missing_students()
