from course_data_db import get_students_by_module
import pandas as pd

data = get_students_by_module("DS102")
df = pd.DataFrame(data)

print("Columns:", df.columns.tolist())
print("Sample rows:")
print(df.head(5))
print("Total rows:", len(df))
