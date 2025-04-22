import pandas as pd
from course_data import data_science_students, software_engineering_students

# ✅ Penalty Keywords (will match even if emojis are present)
PENALTY_KEYWORDS = [
    "Lateness Penalty",
    "Word Count Penalty",
    "Academic Misconduct",
    "Exceptional Circumstances"
]

def has_penalty(penalty_str):
    """Returns True if the penalty string contains any of the defined keywords."""
    if not penalty_str:
        return False
    return any(keyword in penalty_str for keyword in PENALTY_KEYWORDS)

def classify_status(original_status, penalty):
    """Reclassify 'Completed' to 'Completed with Penalty' if a penalty exists."""
    if original_status == "Completed" and has_penalty(penalty):
        return "Completed with Penalty"
    return original_status


# ✅ Software Engineering Data
def get_processed_se_data():
    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.25) + (a2 * 0.25) + (exam * 0.5)
        if "Lateness Penalty" in p1 or "Lateness Penalty" in p2:
            grade *= 0.95
        if "Word Count Penalty" in p1 or "Word Count Penalty" in p2:
            grade *= 0.9
        return round(grade, 2)

    df = pd.DataFrame(software_engineering_students)

    df["Final Grade"] = df.apply(lambda row: calculate_final_grade(
        float(row.get("a1_score", 0)),
        float(row.get("a2_score", 0)),
        float(row.get("exam_score", 0)),
        row.get("a1_penalty", ""),
        row.get("a2_penalty", "")
    ), axis=1)

    df["Assignment 1 Status"] = df.apply(
        lambda row: classify_status(row.get("a1_status", ""), row.get("a1_penalty", "")), axis=1)
    df["Assignment 2 Status"] = df.apply(
        lambda row: classify_status(row.get("a2_status", ""), row.get("a2_penalty", "")), axis=1)

    df["Assignment 1 Penalty"] = df["a1_penalty"]
    df["Assignment 2 Penalty"] = df["a2_penalty"]
    df["Attendance"] = df["attendance"]
    df["Exam Score"] = df["exam_score"]
    df["Exam Status"] = df["exam_status"]
    df["Assignment 1 (Bugs and Fixes)"] = df["a1_score"]
    df["Assignment 2 (Software Architecture)"] = df["a2_score"]
    df["Status"] = df["status"]
    df["ID"] = df["id"]
    df["Student"] = df["name"]

    return df


# ✅ Data Science Data
def get_processed_ds_data():
    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.4) + (a2 * 0.3) + (exam * 0.3)
        if "Lateness Penalty" in p1:
            grade -= a1 * 0.4 * 0.05
        if "Lateness Penalty" in p2:
            grade -= a2 * 0.3 * 0.05
        return round(max(grade, 0), 2)

    df = pd.DataFrame(data_science_students)

    df["Final Grade"] = df.apply(lambda row: calculate_final_grade(
        float(row.get("a1_score", 0)),
        float(row.get("a2_score", 0)),
        float(row.get("exam_score", 0)),
        row.get("a1_penalty", ""),
        row.get("a2_penalty", "")
    ), axis=1)

    df["Assignment 1 Status"] = df.apply(
        lambda row: classify_status(row.get("a1_status", ""), row.get("a1_penalty", "")), axis=1)
    df["Assignment 2 Status"] = df.apply(
        lambda row: classify_status(row.get("a2_status", ""), row.get("a2_penalty", "")), axis=1)

    df["Assignment 1 Penalty"] = df["a1_penalty"]
    df["Assignment 2 Penalty"] = df["a2_penalty"]
    df["Attendance"] = df["attendance"]
    df["Exam Score"] = df["exam_score"]
    df["Exam Status"] = df["exam_status"]
    df["Assignment 1 (Data Analysis)"] = df["a1_score"]
    df["Assignment 2 (Machine Learning)"] = df["a2_score"]
    df["Status"] = df["status"]
    df["ID"] = df["id"]
    df["Student"] = df["name"]

    return df
