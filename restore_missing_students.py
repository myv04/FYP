import sqlite3
from datetime import datetime

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

join_date = "2025-04-27"

# Course mappings
course_map = {
    "SE101": [
        "SE8946,Alice Johnson", "SE5918,Bob Smith", "SE7494,Charlie Davis", "SE1509,David Martinez",
        "SE8253,Eve Brown", "SE1744,Frank Wilson", "SE5043,Grace Taylor", "SE8979,Hank Anderson",
        "SE1968,Ivy Thomas", "SE1852,Jack White", "SE8330,Karen Harris", "SE8811,Leo Martin",
        "SE9771,Mona Clark", "SE5353,Nathan Lewis", "SE1179,Olivia Hall", "SE5838,Peter Allen",
        "SE4247,Quincy Young", "SE4796,Rachel King", "SE3642,Steve Wright", "SE3570,Tina Scott",
        "SE3688,Uma Green", "SE9940,Victor Adams", "SE5462,Wendy Baker", "SE4267,Xander Y. Nelson",
        "SE2196,Yvonne Carter", "SE3056,Zachary Mitchell", "SE3902,Aaron Perez", "SE5236,Bella Roberts",
        "SE9158,Cody Gonzalez", "SE8950,Diana Campbell", "SE1967,Ethan Rodriguez", "SE8256,Fiona Moore",
        "SE4532,George Edwards", "SE1517,Holly Flores", "SE7469,Ian Cooper", "SE8148,Julia Murphy",
        "SE1419,Kevin Reed", "SE6287,Laura Cox", "SE3159,Mike Ward", "SE3655,Nina Peterson",
        "SE9723,Oscar Gray", "SE9035,Paula Jenkins", "SE9083,Quinn Russell", "SE2110,Randy Torres",
        "SE6193,Samantha Stevens", "SE4227,Tommy Parker", "SE1890,Ursula Evans", "SE1314,Vince Morgan",
        "SE5890,Whitney Bell", "SE3935,Xavier Phillips"
    ],
    "DS102": [
        "DS6846,Alex Carter", "DS6478,Bella Sanders", "DS1813,Cameron Hughes", "DS9754,Diana Wright",
        "DS4378,Ethan Parker", "DS9791,Felicity James", "DS2011,Gabriel Lewis", "DS6655,Hannah Stone",
        "DS6446,Ian Turner", "DS8178,Jasmine Collins", "DS2556,Kevin Morris", "DS1387,Lara Watson",
        "DS5339,Michael Griffin", "DS1766,Natalie Cooper", "DS1135,Owen Richardson", "DS5293,Paige Scott",
        "DS4568,Quentin Ramirez", "DS3602,Rebecca Bennett", "DS4981,Stephen Howard", "DS2366,Tracy Bell",
        "DS8924,Ulysses Barnes", "DS2684,Victoria Foster", "DS2674,Walter Henderson", "DS1149,Xander Nelson",
        "DS5583,Yvette Campbell", "DS1563,Zane Mitchell", "DS6404,Amelia Ross", "DS8664,Benjamin Ward",
        "DS9607,Chloe Edwards", "DS5013,David Fisher", "DS2760,Emma Butler", "DS5971,Frederick Murphy",
        "DS2594,Grace Price", "DS1207,Henry Stewart", "DS8709,Isabella Torres", "DS9507,Jackie Peterson",
        "DS1882,Kurt Bailey", "DS9592,Lucy Jenkins", "DS9880,Mason Cooper", "DS6445,Nina Adams",
        "DS8511,Oscar Flores", "DS6948,Penelope Russell", "DS5478,Ryan Powell", "DS1215,Sophia Simmons",
        "DS4834,Theodore White", "DS7831,Ursula Martin", "DS1767,Vince Brown", "DS8872,William Gonzales",
        "DS1907,Xenia Moore", "DS7683,Zoe Walker"
    ]
}

# Get all current student IDs
cursor.execute("SELECT id FROM students")
existing_ids = set(row[0] for row in cursor.fetchall())

# Track insertions
inserted_count = 0

for course_code, students in course_map.items():
    cursor.execute("SELECT id FROM courses WHERE code = ?", (course_code,))
    course = cursor.fetchone()
    if not course:
        print(f"❌ Course {course_code} not found.")
        continue
    course_id = course[0]

    for entry in students:
        sid, name = entry.split(",")
        if sid in existing_ids:
            continue

        email = f"{name.lower().replace(' ', '')}{sid}@uni.com"
        username = name
        values = (
            sid, username, 0, "Not Completed", None, None, "Not Completed", None,
            None, "Not Completed", None, "Active", "Enrolled", "Student",
            join_date, email, sid
        )
        cursor.execute("""
            INSERT INTO students (
                id, username, attendance, exam_status, exam_score,
                a1_score, a1_status, a1_penalty, a2_score, a2_status, a2_penalty,
                status, enrollment_status, role, join_date, email, uni_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, values)

        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (sid, course_id))
        inserted_count += 1

conn.commit()
conn.close()
print(f"✅ {inserted_count} missing students restored.")
