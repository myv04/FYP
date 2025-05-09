import sqlite3
import random

# Connect to your SQLite database
conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS lecturer_assignments (
    lecturer_id TEXT,
    lecturer_name TEXT,
    course_code TEXT,
    module_code TEXT,
    module_week TEXT
)
""")

# Define modules and weeks
module_weeks = {
    "SE201": ["Sprint Planning", "Daily Standups", "Backlog Grooming", "Scrum Events", "Velocity Tracking", "Agile Metrics", "Burndown Charts", "Product Increments", "Retrospectives", "Agile Estimation", "Kanban vs Scrum", "Agile Wrap-up"],
    "SE202": ["HTML Basics", "CSS Styling", "Responsive Design", "JavaScript DOM", "Forms and Validation", "Web Hosting", "REST APIs", "Frontend Frameworks", "Authentication", "Web Security", "Debugging Tools", "Deployment"],
    "SE203": ["Testing Basics", "Unit Tests", "Mocks and Stubs", "Integration Testing", "System Testing", "Acceptance Testing", "Test Automation", "Bug Tracking", "Regression Testing", "Performance Testing", "Security Testing", "Test Reporting"],
    "SE204": ["Cloud Basics", "IaaS & PaaS", "Deployment Models", "Cloud Storage", "Load Balancing", "Auto-scaling", "Monitoring Tools", "CI/CD Pipelines", "Containers", "Security in Cloud", "Cloud Costing", "Capstone Demo"],
    "DS101": ["Data Cleaning", "Feature Engineering", "Model Selection", "Supervised Learning", "Unsupervised Learning", "Neural Networks", "Evaluation Metrics", "Model Deployment", "Overfitting & Underfitting", "Hyperparameter Tuning", "Bias-Variance Tradeoff", "Final Review"],
    "DS102": ["Intro to Big Data", "Hadoop Ecosystem", "Spark Basics", "Data Lakes & Warehouses", "Data Ingestion", "ETL Pipelines", "MapReduce", "Stream Processing", "Data Storage", "Scalability", "Big Data Tools", "Case Study"],
    "DS203": ["DevOps & MLOps", "Model Deployment", "API Integration", "Continuous Delivery", "Dockerization", "Monitoring Models", "Data Drift", "Model Logging", "Scaling Inference", "Deployment Tools", "Model Governance", "Final Review"],
    "DS204": ["Data Ethics Intro", "Bias in AI", "Fairness Metrics", "Case Studies", "Consent Mechanisms", "GDPR", "Data Security", "Responsible AI", "Transparency", "Accountability", "Audit Frameworks", "Wrap-Up"]
}

# Organize lecturers by course
software_lecturers = [
    ("806642", "Heidi Hall"), ("806419", "Joyce Maldonado"), ("807420", "Jennifer Wilkins"),
    ("804072", "Ashley Sherman"), ("804456", "Karen Wagner"), ("805422", "Christina Fox"),
    ("806433", "Heather Malone"), ("800063", "Kelly Woods"), ("802048", "Kimberly Harris"),
    ("801441", "Donna Smith"), ("809281", "Kenneth Scott"), ("805698", "Ashley Flores"),
    ("806162", "Julie Mccarthy"), ("809545", "Brittany Thompson"), ("802443", "Lee Berry"),
    ("809065", "Michael Robles"), ("802578", "Laura Cohen"), ("801363", "Anthony Pearson"),
    ("802402", "Mary Cruz"), ("806828", "Lori Palmer"), ("806618", "Lori Herrera"),
    ("808297", "Jennifer Jones"), ("805485", "Andrew Stevens"), ("808007", "Jennifer Burnett"),
    ("808420", "Lindsay Rodriguez"), ("806731", "Jacqueline Snyder"), ("803170", "Paul Clark"),
    ("805922", "Anthony Ramirez"), ("802126", "John Ramos"), ("804935", "Vincent Griffith")
]

data_lecturers = [
    ("802723", "Heather Simon"), ("806063", "Sheila Guerrero"), ("807012", "Keith Bradley"),
    ("805928", "Harry Burnett"), ("809706", "Jennifer Cross"), ("803984", "Jennifer Wright"),
    ("805410", "Alexa Duran"), ("802829", "Jack Oneill"), ("805522", "Rodney Hutchinson"),
    ("808021", "Christine Newton"), ("809161", "Jennifer Jones"), ("804257", "Albert Keller"),
    ("802085", "Elizabeth Prince"), ("809213", "Tammie Nolan"), ("805988", "Bonnie Thompson"),
    ("802784", "Barbara Palmer"), ("800536", "Nathan Chambers"), ("805258", "Brian Anderson"),
    ("803664", "Megan Rogers"), ("804934", "Sharon Page"), ("801424", "Casey Wright"),
    ("805065", "Jorge Clark"), ("803327", "George Wilson"), ("805282", "Mark Ortega"),
    ("809332", "Mark Sanchez")
]

# Helper to prevent more than 3 lecturers per week
week_assignments = {}

def assign_weeks(module_code):
    weeks = module_weeks[module_code]
    random.shuffle(weeks)
    assigned = []
    for week in weeks:
        count = week_assignments.get((module_code, week), 0)
        if count < 3:
            week_assignments[(module_code, week)] = count + 1
            assigned.append(week)
        if len(assigned) >= random.randint(2, 4):
            break
    return assigned

def assign_lecturers(lecturers, course_code, module_codes):
    assignments = []
    for lecturer_id, name in lecturers:
        module = random.choice(module_codes)
        weeks = assign_weeks(module)
        for week in weeks:
            assignments.append((lecturer_id, name, course_code, module, week))
    return assignments

# Assign
se_assignments = assign_lecturers(software_lecturers, "SE101", ["SE201", "SE202", "SE203", "SE204"])
ds_assignments = assign_lecturers(data_lecturers, "DS102", ["DS101", "DS102", "DS203", "DS204"])
all_assignments = se_assignments + ds_assignments

# Insert into database
cursor.executemany("""
    INSERT INTO lecturer_assignments (lecturer_id, lecturer_name, course_code, module_code, module_week)
    VALUES (?, ?, ?, ?, ?)
""", all_assignments)

conn.commit()
conn.close()

print(f"Inserted {len(all_assignments)} lecturer-week-module assignments.")
