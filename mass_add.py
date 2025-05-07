import requests
import random
from datetime import datetime

# 🔁 Change this if your Flask app runs on a different URL or port
BASE_URL = "http://127.0.0.1:5000"

# Define how many people to add
courses = {
    3: {"course_name": "Software", "students": 450, "tas": 6, "admins": 3},       # course_id 3 = Software
    4: {"course_name": "Data Science", "students": 400, "tas": 6, "admins": 3}    # course_id 4 = Data Science
}

def generate_name():
    first_names = ["Alex", "Taylor", "Jordan", "Casey", "Morgan", "Jamie", "Riley", "Logan", "Skylar", "Quinn"]
    last_names = ["Smith", "Lee", "Brown", "Jones", "Davis", "White", "Moore", "Martin", "Clark", "Hall"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def add_user(course_id, name, role, enrollment_status, course_name):
    url = f"{BASE_URL}/course/{course_id}/add_user"
    data = {
        "name": name,
        "role": role,
        "enrollment_status": enrollment_status,
        "course_name": course_name
    }
    r = requests.post(url, data=data)
    if r.status_code == 200:
        print(f"✅ Added {role}: {name} to {course_name}")
    else:
        print(f"❌ Failed to add {name} — {r.status_code}")

# 🚀 Add everyone
for course_id, info in courses.items():
    course_name = info["course_name"]

    # Students
    for _ in range(info["students"]):
        add_user(course_id, generate_name(), "Student", "Enrolled", course_name)

    # TAs
    for _ in range(info["tas"]):
        add_user(course_id, generate_name(), "Teacher Assistant", "Active", course_name)

    # Admins
    for _ in range(info["admins"]):
        add_user(course_id, generate_name(), "Admin", "Active", course_name)
