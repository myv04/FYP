import sqlite3

def update_students_table():
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    # Add missing columns if they don't already exist
    columns_to_add = {
        "attendance": "INTEGER DEFAULT 0",
        "exam_status": "TEXT DEFAULT ''",
        "exam_score": "REAL DEFAULT 0",
        "a1_score": "REAL DEFAULT 0",
        "a1_status": "TEXT DEFAULT ''",
        "a1_penalty": "TEXT DEFAULT ''",
        "a2_score": "REAL DEFAULT 0",
        "a2_status": "TEXT DEFAULT ''",
        "a2_penalty": "TEXT DEFAULT ''",
        "status": "TEXT DEFAULT 'Active'"
    }

    for column, definition in columns_to_add.items():
        try:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {column} {definition}")
            print(f"✅ Added column: {column}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"ℹ️ Column already exists: {column}")
            else:
                raise

    conn.commit()
    conn.close()
    print("\n🎉 Table updated successfully.")

if __name__ == "__main__":
    update_students_table()
