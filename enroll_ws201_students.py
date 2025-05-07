# enroll_ws201_students.py
import sqlite3
import random

# ✅ IDs from your provided list (first 80 selected)
student_ids = [
    'SE274186', 'SE239278', 'SE550110', 'SE406328', 'SE654033', 'SE831216', 'SE371373', 'SE900421', 'SE880735', 'SE936782',
    'SE693549', 'SE677733', 'SE361046', 'SE256288', 'SE447464', 'SE553174', 'SE681325', 'SE338461', 'SE416298', 'SE495740',
    'SE497862', 'SE329904', 'SE296937', 'SE867328', 'SE157741', 'SE322880', 'SE779042', 'SE869108', 'SE409815', 'SE776205',
    'SE889759', 'SE748961', 'SE853783', 'SE638295', 'SE420881', 'SE311834', 'SE252186', 'SE451795', 'SE129801', 'SE681601',
    'SE611271', 'SE485405', 'SE216427', 'SE513271', 'SE490954', 'SE935858', 'SE563556', 'SE696234', 'SE290113', 'SE643596',
    'SE315348', 'SE440149', 'SE129997', 'SE223149', 'SE207003', 'SE648838', 'SE186012', 'SE106507', 'SE390927', 'SE710357',
    'SE710405', 'SE999109', 'SE535463', 'SE197802', 'SE116722', 'SE541835', 'SE964887', 'SE352635', 'SE751747', 'SE636474',
    'SE802502', 'SE637223', 'SE262820', 'SE236438', 'SE437059', 'SE276725', 'SE175784', 'SE266643', 'SE660712', 'SE152779'
]

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

count = 0

for student_id in student_ids:
    # Enroll into WS201 (ignore if already there)
    cursor.execute("""
        INSERT OR IGNORE INTO module_enrollments (student_id, module_code)
        VALUES (?, ?)
    """, (student_id, 'WS201'))

    # Add or overwrite dashboard-related fields
    cursor.execute("""
        UPDATE students
        SET attendance = ?,
            a1_score = ?,
            a1_status = 'Completed',
            a1_penalty = 'None',
            status = 'Enrolled'
        WHERE id = ?
    """, (
        random.randint(65, 100),
        round(random.uniform(60, 95), 2),
        student_id
    ))

    count += 1

conn.commit()
conn.close()

print(f"✅ Enrolled {count} students into WS201 with full dashboard data.")
