import sqlite3

conn = sqlite3.connect("reports_data.db")
cursor = conn.cursor()

# Table: modules
cursor.execute('''
CREATE TABLE IF NOT EXISTS modules (
    module_code TEXT PRIMARY KEY,
    module_name TEXT NOT NULL
)
''')

# Table: report_data (module metrics)
cursor.execute('''
CREATE TABLE IF NOT EXISTS report_data (
    module_code TEXT PRIMARY KEY,
    avg_attendance INTEGER,
    assignments_completed INTEGER,
    assignments_pending INTEGER,
    current_grade REAL,
    FOREIGN KEY (module_code) REFERENCES modules(module_code)
)
''')

# Table: assessments
cursor.execute('''
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_code TEXT,
    assessment_name TEXT,
    score REAL,
    FOREIGN KEY (module_code) REFERENCES modules(module_code)
)
''')

conn.commit()
conn.close()

print("✅ reports_data.db initialized with full schema.")
