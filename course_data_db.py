
import sqlite3
import pandas as pd



def get_students_by_course(course_id):
    conn = sqlite3.connect("courses.db")
    df = pd.read_sql_query("""
        SELECT DISTINCT s.*, e.course_id
        FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = ? AND s.enrollment_status != 'Removed'
    """, conn, params=(course_id,))
    conn.close()

    if df.empty:
        return []

    df.rename(columns={
        "username": "name",
        "a1_score": "Assignment 1 (Bugs and Fixes)",
        "a1_status": "Assignment 1 Status",
        "a1_penalty": "Assignment 1 Penalty",
        "a2_score": "Assignment 2 (Software Architecture)",
        "a2_status": "Assignment 2 Status",
        "a2_penalty": "Assignment 2 Penalty",
        "exam_score": "Exam Score",
        "exam_status": "Exam Status",       
        "attendance": "Attendance (%)",
        "status": "Status"
    }, inplace=True)

    return df.to_dict(orient="records")




def get_students_by_module(module_code):
    conn = sqlite3.connect("courses.db")

    df = pd.read_sql_query("""
        SELECT DISTINCT s.id AS ID,
                        s.username AS Student,
                        s.attendance AS "Attendance (%)",
                        s.status AS Status,
                        s.a1_score AS "Assignment 1 (Data Lakes)",
                        s.a1_status AS "Assignment 1 Status",
                        s.a1_penalty AS "Assignment 1 Penalty"
        FROM students s
        JOIN module_enrollments me ON s.id = me.student_id
        WHERE me.module_code = ? AND LOWER(s.role) = 'student'
    """, conn, params=(module_code,))

    conn.close()

    def calculate_final_grade(score, penalty):
        grade = float(score or 0)
        if penalty:
            if "Lateness Penalty" in penalty:
                grade *= 0.95
            if "Word Count Penalty" in penalty:
                grade *= 0.9
        return round(grade, 2)

    if not df.empty:
        df["Final Grade"] = df.apply(lambda row: calculate_final_grade(
            row["Assignment 1 (Data Lakes)"], row["Assignment 1 Penalty"]
        ), axis=1)

    return df.to_dict(orient="records")

def get_students_for_web_systems():
    import sqlite3
    import pandas as pd

    
    excluded_ids = [
        'SE8946', 'SE5918', 'SE7494', 'SE1509', 'SE8253', 'SE1744', 'SE5043', 'SE8979', 'SE1968', 'SE1852',
        'SE8330', 'SE8811', 'SE9771', 'SE5353', 'SE1179', 'SE5838', 'SE4247', 'SE4796', 'SE3642', 'SE3570',
        'SE3688', 'SE9940', 'SE5462', 'SE4267', 'SE2196', 'SE3056', 'SE3902', 'SE5236', 'SE9158', 'SE8950',
        'SE1967', 'SE8256', 'SE4532', 'SE1517', 'SE7469', 'SE8148', 'SE1419', 'SE6287', 'SE3159', 'SE3655',
        'SE9723', 'SE9035', 'SE9083', 'SE2110', 'SE6193', 'SE4227', 'SE1890', 'SE1314', 'SE5890', 'SE3935'
    ]

    conn = sqlite3.connect("courses.db")
    df = pd.read_sql_query(f"""
        SELECT DISTINCT s.id AS ID,
                        s.username AS Student,
                        s.attendance AS "Attendance (%)",
                        s.status AS Status,
                        s.a1_score AS "Assignment 1 (Web Tech)",
                        s.a1_status AS "Assignment 1 Status",
                        s.a1_penalty AS "Assignment 1 Penalty"
        FROM students s
        JOIN module_enrollments me ON s.id = me.student_id
        WHERE me.module_code = 'WS201'
          AND LOWER(s.role) = 'student'
          AND s.id NOT IN ({','.join(['?']*len(excluded_ids))})
          AND s.a1_score IS NOT NULL
          AND s.a1_status IS NOT NULL
          AND s.a1_penalty IS NOT NULL
    """, conn, params=excluded_ids)
    conn.close()

    if df.empty:
        return []

    def calculate_final(score, penalty):
        grade = float(score or 0)
        if penalty:
            if "Lateness Penalty" in penalty:
                grade *= 0.95
            if "Word Count Penalty" in penalty:
                grade *= 0.9
        return round(grade, 2)

    df["Final Grade"] = df.apply(lambda row: calculate_final(
        row["Assignment 1 (Web Tech)"], row["Assignment 1 Penalty"]
    ), axis=1)

    return df.to_dict(orient="records")

def calculate_final_grade_for_df(df):
    def calculate(row):
        try:
            a1 = float(row.get("a1_score", 0) or 0)
            a2 = float(row.get("a2_score", 0) or 0)
            exam = float(row.get("exam_score", 0) or 0)

            grade = (a1 * 0.25) + (a2 * 0.25) + (exam * 0.5)

            p1 = row.get("a1_penalty", "")
            p2 = row.get("a2_penalty", "")
            if "Lateness Penalty" in str(p1):
                grade *= 0.95
            if "Word Count Penalty" in str(p1):
                grade *= 0.9
            if "Lateness Penalty" in str(p2):
                grade *= 0.95
            if "Word Count Penalty" in str(p2):
                grade *= 0.9

            return round(grade, 2)
        except Exception:
            return 0
    df["Final Grade"] = df.apply(calculate, axis=1)
    return df

