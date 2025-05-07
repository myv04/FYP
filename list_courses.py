import sqlite3

def list_courses():
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    rows = cursor.execute("SELECT id, name, code FROM courses").fetchall()
    print("\n📚 Available courses:")
    for row in rows:
        print(f"  ID: {row[0]} | Name: {row[1]} | Code: {row[2]}")
    conn.close()

if __name__ == "__main__":
    list_courses()
