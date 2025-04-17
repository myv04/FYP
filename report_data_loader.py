import sqlite3

def fetch_module_data(module_code):
    conn = sqlite3.connect("reports_data.db")
    cursor = conn.cursor()

    # Get module info
    cursor.execute("SELECT module_name FROM modules WHERE module_code = ?", (module_code,))
    row = cursor.fetchone()
    if not row:
        return None
    module_name = row[0]

    # Get report metrics
    cursor.execute("""
        SELECT avg_attendance, assignments_completed, assignments_pending, current_grade
        FROM report_data WHERE module_code = ?
    """, (module_code,))
    data = cursor.fetchone()
    if not data:
        return None

    metrics = [
        ("Average Attendance", data[0]),
        ("Completed Assignments", data[1]),
        ("Pending Assignments", data[2]),
        ("Current Grade (%)", data[3])
    ]

    # Get assessments
    cursor.execute("""
        SELECT assessment_name, score FROM assessments WHERE module_code = ?
    """, (module_code,))
    assignments = cursor.fetchall()

    conn.close()

    return {
        "module_name": module_name,
        "module_code": module_code,
        "metrics": metrics,
        "assignments": assignments
    }
