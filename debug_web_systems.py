from course_data_db import get_students_for_web_systems
import pandas as pd

df = pd.DataFrame(get_students_for_web_systems())
print("🟢 Columns:", df.columns.tolist())
print("🔍 Sample data:\n", df.head())
