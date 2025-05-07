import requests
import random
from faker import Faker

fake = Faker()

# Your Flask App URL
BASE_URL = "http://127.0.0.1:5000"

# Course Info - update these if needed
SOFTWARE_COURSE_ID = 3
DATA_SCIENCE_COURSE_ID = 4

# How many lecturers to add
NUM_SOFTWARE_LECTURERS = 30
NUM_DATASCIENCE_LECTURERS = 25

def add_lecturers(course_id, count, course_name):
    for _ in range(count):
        name = fake.name()
        payload = {
            "name": name,
            "role": "Lecturer",
            "enrollment_status": "Active",
            "course_name": course_name
        }

        response = requests.post(f"{BASE_URL}/course/{course_id}/add_user", data=payload)

        if response.ok:
            print(f"✅ Added lecturer: {name} to {course_name}")
        else:
            print(f"❌ Failed to add {name}: {response.status_code} - {response.text}")

# Add 30 lecturers to Software
add_lecturers(SOFTWARE_COURSE_ID, NUM_SOFTWARE_LECTURERS, "BSc Software Engineering")

# Add 25 lecturers to Data Science
add_lecturers(DATA_SCIENCE_COURSE_ID, NUM_DATASCIENCE_LECTURERS, "BSc Data Science")
