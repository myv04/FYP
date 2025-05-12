import sqlite3

def clean_se_ds_students(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Find IDs of SE/DS students
    cur.execute("""
        SELECT id FROM students
        WHERE role = 'Student'
        AND (uni_id LIKE 'SE%' OR uni_id LIKE 'DS%')
    """)
    student_ids = [row[0] for row in cur.fetchall()]

    if not student_ids:
        print("✅ No SE or DS students found to delete.")
        conn.close()
        return

    # Delete related enrollments
    cur.executemany("DELETE FROM enrollments WHERE student_id = ?", [(sid,) for sid in student_ids])

    # Delete the students themselves
    cur.executemany("DELETE FROM students WHERE id = ?", [(sid,) for sid in student_ids])

    conn.commit()
    conn.close()
    print(f"✅ Deleted {len(student_ids)} SE/DS students and their enrollments.")

# Run it
clean_se_ds_students("courses.db")
