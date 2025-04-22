from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import pandas as pd
import os
from models import db, User
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from flask import send_file
from flask_login import login_required
from flask import Flask
from flask import send_file
import zipfile
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import random
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import render_template
import sqlite3  # ✅ Using SQLite for simplicity
import sqlite3
from flask import Flask, render_template, redirect, url_for, request, jsonify
from faker import Faker
from datetime import datetime, timedelta
from report_data_loader import fetch_module_data
import csv
from student_data_loader import fetch_student_dashboard
from flask import session
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from data_persistence import load_data
from helpers.shared_dashboard_data import get_processed_se_data, get_processed_ds_data
from openpyxl.utils import get_column_letter
import json
from flask import send_file, make_response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful!", "success")
            if user.role == "student":
                return redirect(url_for('home_student'))
            elif user.role == "lecturer":
                return redirect(url_for('home_lecturer'))
            else:
                return redirect(url_for('home_admin'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)  # 👈 this clears existing flash messages
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/home_student')
@login_required
def home_student():
    return render_template('home_student.html', user=current_user)

@app.route('/home_lecturer')
@login_required
def home_lecturer():
    return render_template('home_lecturer.html', user=current_user)

@app.route('/home_admin')
@login_required
def home_admin():
    return render_template('home_admin.html', user=current_user)

@app.route('/student_profile')
@login_required
def student_profile():
    if current_user.role != "student":
        flash("Unauthorized Access", "danger")
        return redirect(url_for('index'))
    return render_template('student_profile.html', user=current_user)

@app.route('/student/modules')
@login_required
def student_modules():
    return render_template('student_modules.html')

@app.route('/data_structures_dashboard')
@login_required
def data_structures_dashboard():
    return render_template('data_structures_dashboard.html')

@app.route('/webdev_dashboard')
@login_required
def webdev_dashboard():
    return render_template('webdev_dashboard.html')

@app.route('/ai_dashboard')
@login_required
def ai_dashboard():
    return render_template('ai_dashboard.html')

@app.route('/db_dashboard')
@login_required
def db_dashboard():
    return render_template('db_dashboard.html')

@app.route('/cybersecurity_dashboard')
@login_required
def cybersecurity_dashboard():
    return render_template('cybersecurity_dashboard.html')

@app.route('/attendance_dashboard')
@login_required
def attendance_dashboard():
    return render_template('attendance_dashboard.html')

@app.route('/software_engineering_dashboard')
@login_required
def software_engineering_dashboard():
    return render_template('software_engineering_dashboard.html')

@app.route('/data_science_dashboard')
@login_required
def data_science_dashboard_page():
    return render_template('data_science_dashboard.html')

@app.route('/course_registers')
def course_registers_page():
    return render_template('course_registers.html')

@app.route('/lecturer_profile')
@login_required
def lecturer_profile():
    return render_template('lecturer_profile.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')  # Replace with the actual template or logic for courses

@app.route('/students')
def students():
    return render_template('students.html')  # Replace with the actual template or logic for students

@app.route('/reports')
def reports():
    return render_template('reports.html')  # Replace with the actual template or logic for reports

@app.route('/export')
def export():
    return render_template('export.html')  # Replace with the actual template or logic for export

@app.route('/students_overview')
@login_required
def students_overview_page():
    return render_template('students_overview.html')

@app.route("/student_attendance_insights/")
@login_required
def student_attendance_insights_page():
    return render_template("student_attendance_insights.html")

@app.route('/export_lecturer')
@login_required
def export_lecturer():
    return render_template('lecturer_export.html')

@app.route('/download_excel_overview_dashboard')
@login_required
def download_excel_overview_dashboard():
    return send_file("path/to/overview_dashboard.xlsx", as_attachment=True)

@app.route('/download_csv_overview_dashboard')
@login_required
def download_csv_overview_dashboard():
    return send_file("path/to/overview_dashboard.csv", as_attachment=True)

@app.route('/download_excel_software_engineering')
@login_required
def download_excel_software_engineering():
    return send_file("path/to/software_engineering.xlsx", as_attachment=True)

@app.route('/download_csv_software_engineering')
@login_required
def download_csv_software_engineering():
    return send_file("path/to/software_engineering.csv", as_attachment=True)

@app.route('/download_excel_data_science')
@login_required
def download_excel_data_science():
    return send_file("path/to/data_science.xlsx", as_attachment=True)

@app.route('/download_csv_data_science')
@login_required
def download_csv_data_science():
    return send_file("path/to/data_science.csv", as_attachment=True)

@app.route('/download_excel_students_overview')
@login_required
def download_excel_students_overview():
    return send_file("path/to/students_overview.xlsx", as_attachment=True)

@app.route('/download_csv_students_overview')
@login_required
def download_csv_students_overview():
    return send_file("path/to/students_overview.csv", as_attachment=True)

@app.route('/download_excel_student_attendance_insights')
@login_required
def download_excel_student_attendance_insights():
    return send_file("path/to/student_attendance_insights.xlsx", as_attachment=True)

@app.route('/download_csv_student_attendance_insights')
@login_required
def download_csv_student_attendance_insights():
    return send_file("path/to/student_attendance_insights.csv", as_attachment=True)

def export_file(df, filename, file_type="excel"):
    if file_type == "excel":
        file_path = f"{filename}.xlsx"
        df.to_excel(file_path, index=False)
    else:
        file_path = f"{filename}.csv"
        df.to_csv(file_path, index=False)

    return send_file(file_path, as_attachment=True)


# EXPORT for STUDENT-SIDE MODULES #
def generate_module_report_from_dict(module_data, file_type):
    # Create clean filename based on module name
    safe_name = module_data['module_name'].replace(" ", "_")  # You can also use .replace(" ", "") if preferred
    file_path = f"{safe_name}_Report.{file_type}"
    metrics = module_data["metrics"]
    assignments = module_data["assignments"]

    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = module_data['module_name']
        ws.column_dimensions["A"].width = 40
        ws.column_dimensions["B"].width = 20

        ws.merge_cells("A1:B1")
        ws["A1"] = f"MODULE: {module_data['module_name']}"
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:B2")
        ws["A2"] = f"Module Code: {module_data['module_code']}"
        ws["A2"].alignment = Alignment(horizontal="center")

        thin_border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )

        for i, (metric, value) in enumerate(metrics):
            ws[f"A{4 + i}"] = metric
            ws[f"B{4 + i}"] = value
            ws[f"A{4 + i}"].border = thin_border
            ws[f"B{4 + i}"].border = thin_border

        ws["A8"] = "ASSESSMENT"
        ws["B8"] = "SCORE %"
        ws["A8"].font = Font(bold=True)
        ws["B8"].font = Font(bold=True)

        for i, (title, score) in enumerate(assignments):
            ws[f"A{9 + i}"] = title
            ws[f"B{9 + i}"] = score if score is not None else ""

        table = Table(displayName="ScoresTable", ref=f"A8:B{8 + len(assignments)}")
        style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
        table.tableStyleInfo = style
        ws.add_table(table)

        wb.save(file_path)
        return send_file(file_path, as_attachment=True, download_name=f"{safe_name}_Report.xlsx")

    elif file_type == "csv":
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([f"MODULE: {module_data['module_name']}"])
            writer.writerow([f"Module Code: {module_data['module_code']}"])
            writer.writerow([])
            writer.writerow(["Metric", "Value"])
            for metric, value in metrics:
                writer.writerow([metric, value])
            writer.writerow([])
            writer.writerow(["ASSESSMENT", "SCORE %"])
            for title, score in assignments:
                writer.writerow([title, score if score is not None else ""])

        return send_file(file_path, as_attachment=True, download_name=f"{safe_name}_Report.csv")

@app.route('/download_excel_ai')
@login_required
def download_excel_ai():
    module = fetch_module_data("CS203")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "xlsx")

@app.route('/download_csv_ai')
@login_required
def download_csv_ai():
    module = fetch_module_data("CS203")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "csv")

@app.route('/download_excel_webdev')
@login_required
def download_excel_webdev():
    module = fetch_module_data("CS202")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "xlsx")

@app.route('/download_csv_webdev')
@login_required
def download_csv_webdev():
    module = fetch_module_data("CS202")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "csv")

@app.route('/download_excel_db')
@login_required
def download_excel_db():
    module = fetch_module_data("CS204")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "xlsx")

@app.route('/download_csv_db')
@login_required
def download_csv_db():
    module = fetch_module_data("CS204")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "csv")

@app.route('/download_excel_cybersecurity')
@login_required
def download_excel_cybersecurity():
    module = fetch_module_data("CS205")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "xlsx")

@app.route('/download_csv_cybersecurity')
@login_required
def download_csv_cybersecurity():
    module = fetch_module_data("CS205")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "csv")

@app.route('/download_excel_dsa')
@login_required
def download_excel_dsa():
    module = fetch_module_data("CS201")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "xlsx")

@app.route('/download_csv_dsa')
@login_required
def download_csv_dsa():
    module = fetch_module_data("CS201")
    if not module:
        return "Module not found", 404
    return generate_module_report_from_dict(module, "csv")


####################################################################################################################
def generate_student_dashboard_report(data, file_type):
    file_path = f"Student_Performance_Report.{file_type}"

    grades = data["grades"]
    assignments = data["assignments"]
    exams = data["exams"]
    deadlines = data["deadlines"]

    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Student Dashboard"

        # Styles
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        completed_fill = PatternFill(start_color="92D050", end_color="92D050", fill_type="solid")
        not_completed_fill = PatternFill(start_color="FF5050", end_color="FF5050", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        # Header
        ws.merge_cells("A1:D1")
        ws["A1"] = "STUDENT PERFORMANCE DASHBOARD"
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:D2")
        ws["A2"] = f"Student: {data['student_name']}"
        ws["A2"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A3:D3")
        ws["A3"] = f"Student ID: {data['student_id']}"
        ws["A3"].alignment = Alignment(horizontal="center")

        ws["A5"] = "Average Attendance"
        ws["B5"] = data["attendance"]

        # Grades Table
        ws.merge_cells("A7:D7")
        ws["A7"] = "Grades by Module"
        ws["A7"].fill = header_fill
        ws["A7"].alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Grade %"])
        for row in grades:
            ws.append(row)

        for row in ws.iter_rows(min_row=9, max_row=9 + len(grades), min_col=1, max_col=2):
            for cell in row:
                cell.border = border

        # Assignments
        ws.append([""])
        ws.merge_cells(f"A{ws.max_row + 1}:D{ws.max_row + 1}")
        ws.cell(row=ws.max_row, column=1).value = "Assignments"
        ws.cell(row=ws.max_row, column=1).fill = header_fill
        ws.cell(row=ws.max_row, column=1).alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Assignment Name", "Score", "Status"])
        for row in assignments:
            ws.append(row)

        for row in ws.iter_rows(min_row=ws.max_row - len(assignments), max_row=ws.max_row, min_col=1, max_col=4):
            for cell in row:
                cell.border = border
                if cell.column == 4:
                    if cell.value == "Completed":
                        cell.fill = completed_fill
                    elif cell.value in ["Not Completed", "Not Started"]:
                        cell.fill = not_completed_fill

        # Exams
        ws.append([""])
        ws.merge_cells(f"A{ws.max_row + 1}:D{ws.max_row + 1}")
        ws.cell(row=ws.max_row, column=1).value = "Exams"
        ws.cell(row=ws.max_row, column=1).fill = header_fill
        ws.cell(row=ws.max_row, column=1).alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Exam Name", "Score", "Status"])
        for row in exams:
            ws.append(row)

        for row in ws.iter_rows(min_row=ws.max_row - len(exams), max_row=ws.max_row, min_col=1, max_col=4):
            for cell in row:
                cell.border = border
                if cell.column == 4 and cell.value == "Not Completed":
                    cell.fill = not_completed_fill

        # Deadlines
        ws.append([""])
        ws.merge_cells(f"A{ws.max_row + 1}:D{ws.max_row + 1}")
        ws.cell(row=ws.max_row, column=1).value = "Upcoming Deadlines"
        ws.cell(row=ws.max_row, column=1).fill = header_fill
        ws.cell(row=ws.max_row, column=1).alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Assignment Name", "Deadline Date", "Days Left"])
        for row in deadlines:
            ws.append(row)

        for row in ws.iter_rows(min_row=ws.max_row - len(deadlines), max_row=ws.max_row, min_col=1, max_col=4):
            for cell in row:
                cell.border = border

        wb.save(file_path)
        return send_file(file_path, as_attachment=True, download_name=file_path)

    # CSV version
    elif file_type == "csv":
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["STUDENT PERFORMANCE DASHBOARD"])
            writer.writerow([f"Student: {data['student_name']}"])
            writer.writerow([f"Student ID: {data['student_id']}"])
            writer.writerow([])
            writer.writerow(["Average Attendance", data["attendance"]])
            writer.writerow([])

            writer.writerow(["Module Name", "Grade %"])
            for row in grades:
                writer.writerow(row)
            writer.writerow([])

            writer.writerow(["Module Name", "Assignment Name", "Score", "Status"])
            for row in assignments:
                writer.writerow(row)
            writer.writerow([])

            writer.writerow(["Module Name", "Exam Name", "Score", "Status"])
            for row in exams:
                writer.writerow(row)
            writer.writerow([])

            writer.writerow(["Module Name", "Assignment Name", "Deadline Date", "Days Left"])
            for row in deadlines:
                writer.writerow(row)

        return send_file(file_path, as_attachment=True, download_name=file_path)









@app.route('/download_excel_student_performance')
@login_required
def download_excel_student_performance():
    data = fetch_student_dashboard()
    return generate_student_dashboard_report(data, "xlsx")

@app.route('/download_csv_student_performance')
@login_required
def download_csv_student_performance():
    data = fetch_student_dashboard()
    return generate_student_dashboard_report(data, "csv")




@app.route('/download_excel_attendance')
@login_required
def download_excel_attendance():
    conn = sqlite3.connect("reports_data.db")
    df = pd.read_sql_query("""
        SELECT m.module_name AS 'Module', r.avg_attendance AS 'Attendance (%)'
        FROM report_data r
        JOIN modules m ON r.module_code = m.module_code
    """, conn)
    conn.close()
    return export_file(df, "Attendance_Report", "xlsx")

@app.route('/download_csv_attendance')
@login_required
def download_csv_attendance():
    conn = sqlite3.connect("reports_data.db")
    df = pd.read_sql_query("""
        SELECT m.module_name AS 'Module', r.avg_attendance AS 'Attendance (%)'
        FROM report_data r
        JOIN modules m ON r.module_code = m.module_code
    """, conn)
    conn.close()
    return export_file(df, "Attendance_Report", "csv")

###############################################################################################################################









# lecturers exports
# ✅ Function to generate Lecturer Dashboard Export with updated data
def generate_lecturer_dashboard_report(file_type="xlsx"):
    file_path = f"overview_dashboard.{file_type}"

    # ✅ Use processed DataFrames
    se_df = get_processed_se_data()
    ds_df = get_processed_ds_data()

    # ✅ Compute metrics
    se_avg = se_df["Final Grade"].mean() if not se_df.empty else 0
    ds_avg = ds_df["Final Grade"].mean() if not ds_df.empty else 0
    avg_attendance = (se_df["Attendance"].mean() + ds_df["Attendance"].mean()) / 2 if not se_df.empty and not ds_df.empty else 0
    remaining_attendance = round(100 - avg_attendance, 2)

    # ✅ Metrics Table
    metrics = [
        ["Metric", "Value"],
        ["Average Attendance (%)", round(avg_attendance, 2)],
        ["Remaining Attendance (%)", remaining_attendance],
        ["Software Engineering Avg Score (%)", round(se_avg, 2)],
        ["Data Science Avg Score (%)", round(ds_avg, 2)]
    ]

    # ✅ Assignment Stats (from live data)
    def get_status_counts(df, assignment):
        return df[assignment].value_counts().to_dict()

    assignments = [
        ["Assignment", "Completed", "Completed with Penalty", "Not Completed", "Absent"],
        ["Agile Development - Assignment 1 (Bugs and Fixes)"] +
        [get_status_counts(se_df, "Assignment 1 Status").get(k, 0) for k in ["Completed", "Completed with Penalty", "Not Completed", "Absent"]],
        ["Agile Development - Assignment 2 (Software Architecture)"] +
        [get_status_counts(se_df, "Assignment 2 Status").get(k, 0) for k in ["Completed", "Completed with Penalty", "Not Completed", "Absent"]],
        ["Machine Learning - Assignment 1 (Data Analysis)"] +
        [get_status_counts(ds_df, "Assignment 1 Status").get(k, 0) for k in ["Completed", "Completed with Penalty", "Not Completed", "Absent"]],
        ["Machine Learning - Assignment 2 (Machine Learning)"] +
        [get_status_counts(ds_df, "Assignment 2 Status").get(k, 0) for k in ["Completed", "Completed with Penalty", "Not Completed", "Absent"]],
    ]

    # ✅ Export Logic
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Lecturer Overview Report"

        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'),
                        top=Side(style='thin'), bottom=Side(style='thin'))

        # 📌 Title
        ws.merge_cells("A1:B1")
        ws["A1"] = "Lecturer Dashboard Overview"
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        # 📌 Metrics Table
        for row_idx, row in enumerate(metrics, start=3):
            ws.append(row)
            ws[f"A{row_idx}"].border = border
            ws[f"B{row_idx}"].border = border
            if row_idx == 3:
                ws[f"A{row_idx}"].fill = header_fill
                ws[f"B{row_idx}"].fill = header_fill

        # 📌 Assignments Table
        ws.append([""])  # Spacer
        start_row = len(metrics) + 5
        for row_idx, row in enumerate(assignments, start=start_row):
            ws.append(row)
            for col in range(1, len(row) + 1):
                cell = ws.cell(row=row_idx, column=col)
                cell.border = border
                if row_idx == start_row:
                    cell.fill = header_fill

        wb.save(file_path)
        return file_path

    elif file_type == "csv":
        df_metrics = pd.DataFrame(metrics[1:], columns=metrics[0])
        df_assignments = pd.DataFrame(assignments[1:], columns=assignments[0])

        with open(file_path, "w") as f:
            df_metrics.to_csv(f, index=False)
            f.write("\n")
            df_assignments.to_csv(f, index=False)

        return file_path

    return None


# ✅ Flask Routes to Export Lecturer's Performance Dashboard
@app.route('/download_excel_lecturer_dashboard')
@login_required
def download_excel_lecturer_dashboard():
    file_path = generate_lecturer_dashboard_report("xlsx")
    return send_file(file_path, as_attachment=True, download_name="Lecturer_Overview_Dashboard.xlsx")


@app.route('/download_csv_lecturer_dashboard')
@login_required
def download_csv_lecturer_dashboard():
    file_path = generate_lecturer_dashboard_report("csv")
    return send_file(file_path, as_attachment=True, download_name="Lecturer_Overview_Dashboard.csv")

# ✅ Function to generate Software Engineering Dashboard Export
def generate_software_engineering_report(file_type="excel"):
    file_path = f"software_engineering_dashboard.{file_type}"

    # ✅ Get live processed data
    df = get_processed_se_data()

    # ✅ Clean up duplicates — only keep needed, nicely formatted columns
    df = df[[
        "ID", "Student", "Final Grade", "Attendance", "Exam Status", "Exam Score",
        "Assignment 1 (Bugs and Fixes)", "Assignment 1 Status", "Assignment 1 Penalty",
        "Assignment 2 (Software Architecture)", "Assignment 2 Status", "Assignment 2 Penalty",
        "Status"
    ]]

    # ✅ Excel Export
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Software Eng Dashboard"

        # ✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'),
                        top=Side(style='thin'), bottom=Side(style='thin'))

        # ✅ Title
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(df.columns))
        title_cell = ws.cell(row=1, column=1, value="Software Engineering Dashboard Report")
        title_cell.font = Font(bold=True, size=14)
        title_cell.alignment = Alignment(horizontal="center")

        # ✅ Headers
        for col_num, column_title in enumerate(df.columns, start=1):
            cell = ws.cell(row=2, column=col_num, value=column_title)
            cell.fill = header_fill
            cell.border = border
            cell.alignment = Alignment(horizontal="center")

        # ✅ Data Rows
        for row_idx, row in enumerate(df.itertuples(index=False), start=3):
            for col_idx, value in enumerate(row, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                cell.border = border

        with BytesIO() as b:
            wb.save(b)
            return b.getvalue()

    # ✅ CSV Export
    elif file_type == "csv":
        return df.to_csv(index=False).encode("utf-8")

    return None

@app.route('/download_excel_software_engineering_dashboard')
@login_required
def download_excel_software_engineering_dashboard():
    excel_data = generate_software_engineering_report("xlsx")
    return send_file(
        BytesIO(excel_data),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Software_Engineering_Report.xlsx'
    )

@app.route('/download_csv_software_engineering_dashboard')
@login_required
def download_csv_software_engineering_dashboard():
    csv_data = generate_software_engineering_report("csv")
    return send_file(
        BytesIO(csv_data),
        mimetype='text/csv',
        as_attachment=True,
        download_name='Software_Engineering_Report.csv'
    )


# ✅ Function to generate Data Science Dashboard Export
def generate_data_science_report(file_type="excel"):
    file_path = f"data_science_dashboard.{file_type}"

    # ✅ Get live data
    df = get_processed_ds_data()

    # ✅ Only include clean, export-friendly columns
    df = df[[
        "ID", "Student", "Final Grade", "Attendance", "Exam Status", "Exam Score",
        "Assignment 1 (Data Analysis)", "Assignment 1 Status", "Assignment 1 Penalty",
        "Assignment 2 (Machine Learning)", "Assignment 2 Status", "Assignment 2 Penalty",
        "Status"
    ]]

    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data Science Dashboard"

        # ✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'),
                        top=Side(style='thin'), bottom=Side(style='thin'))

        # ✅ Title at top
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(df.columns))
        title_cell = ws.cell(row=1, column=1, value="Data Science Dashboard Report")
        title_cell.font = Font(bold=True, size=14)
        title_cell.alignment = Alignment(horizontal="center")

        # ✅ Headers
        for col_num, column_title in enumerate(df.columns, start=1):
            cell = ws.cell(row=2, column=col_num, value=column_title)
            cell.fill = header_fill
            cell.border = border
            cell.alignment = Alignment(horizontal="center")

        # ✅ Data
        for row_idx, row in enumerate(df.itertuples(index=False), start=3):
            for col_idx, value in enumerate(row, start=1):
                ws.cell(row=row_idx, column=col_idx, value=value).border = border

        with BytesIO() as b:
            wb.save(b)
            return b.getvalue()

    elif file_type == "csv":
        return df.to_csv(index=False).encode("utf-8")

    return None

# ✅ Flask Routes to Export Data Science Report
@app.route('/download_excel_data_science_dashboard')
@login_required
def download_excel_data_science_dashboard():
    excel_data = generate_data_science_report("xlsx")
    return send_file(
        BytesIO(excel_data),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Data_Science_Report.xlsx'
    )

@app.route('/download_csv_data_science_dashboard')
@login_required
def download_csv_data_science_dashboard():
    csv_data = generate_data_science_report("csv")
    return send_file(
        BytesIO(csv_data),
        mimetype='text/csv',
        as_attachment=True,
        download_name='Data_Science_Report.csv'
    )



def generate_students_overview_report(file_type="xlsx"):
    try:
        se_data = load_data("software_engineering.json")
        ds_data = load_data("data_science.json")

        def flatten(data):
            flat = []
            for item in data:
                if isinstance(item, list):
                    flat.extend(item)
                elif isinstance(item, dict):
                    flat.append(item)
            return flat

        se_data = flatten(se_data)
        ds_data = flatten(ds_data)

    except Exception as e:
        print("❌ Error loading data:", e)
        return None

    for row in se_data:
        row["Course"] = "Software Engineering"
    for row in ds_data:
        row["Course"] = "Data Science"

    df_se = pd.DataFrame(se_data)
    df_ds = pd.DataFrame(ds_data)
    df = pd.concat([df_se, df_ds], ignore_index=True)

    df.rename(columns={
        "name": "Student",
        "Final Grade": "Final Grade",
        "Attendance": "Attendance",
        "attendance": "Attendance",
        "exam_score": "Exam Score",
        "id": "ID"
    }, inplace=True)

    for col in ["Final Grade", "Attendance", "Exam Score"]:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    # === Calculated Tables ===
    avg_grades = df.groupby("Course")["Final Grade"].mean().reset_index().rename(columns={"Final Grade": "Average Grade (%)"})
    avg_attendance = df.groupby("Course")["Attendance"].mean().reset_index().rename(columns={"Attendance": "Average Attendance (%)"})

    # ✅ At-risk = below 60
    at_risk = df[df["Final Grade"] < 60][["Student", "Course", "Final Grade"]].rename(columns={"Final Grade": "Grade"})

    # ✅ Top 5 performers per course
    top_se = df_se.sort_values("Final Grade", ascending=False).head(5)[["Student", "Course", "Final Grade"]]
    top_ds = df_ds.sort_values("Final Grade", ascending=False).head(5)[["Student", "Course", "Final Grade"]]
    top = pd.concat([top_se, top_ds]).rename(columns={"Final Grade": "Grade"})

    # ✅ Grade Distribution Table
    def get_grade_band(score):
        if score >= 70:
            return "100-70%"
        elif score >= 60:
            return "70-60%"
        elif score >= 50:
            return "60-50%"
        else:
            return "50-40%"

    df["Grade Range"] = df["Final Grade"].apply(get_grade_band)
    grade_dist = df.groupby(["Course", "Grade Range"]).size().reset_index(name="Count")

    # ✅ Mocked Performance Comparison (adjust if dynamic later)
    performance_comparison = pd.DataFrame({
        "Metric": ["Assignments", "Exams"],
        "Software Engineering": [78, 85],
        "Data Science": [74, 82]
    })

    # === Excel Export ===
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students Overview"

        title_font = Font(size=14, bold=True)
        header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        border = Border(left=Side(style="thin"), right=Side(style="thin"),
                        top=Side(style="thin"), bottom=Side(style="thin"))

        def write_table(start_row, start_col, title, df_table):
            col_offset = start_col
            row = start_row
            ws.merge_cells(start_row=row, start_column=col_offset, end_row=row, end_column=col_offset + len(df_table.columns) - 1)
            title_cell = ws.cell(row=row, column=col_offset, value=title)
            title_cell.font = Font(bold=True)
            row += 1

            for col_idx, header in enumerate(df_table.columns, start=col_offset):
                cell = ws.cell(row=row, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = Font(bold=True)
                cell.border = border

            for _, record in df_table.iterrows():
                row += 1
                for col_idx, value in enumerate(record, start=col_offset):
                    cell = ws.cell(row=row, column=col_idx, value=value)
                    cell.border = border

            return row + 2

        # === Report Layout ===
        row = 2
        row = write_table(row, 2, "📊 Average Grade per Course", avg_grades)
        row = write_table(row, 2, "📉 Average Attendance per Course", avg_attendance)
        row = write_table(row, 2, "📈 Grade Distribution by Course", grade_dist)
        row = write_table(row, 2, "📋 Performance Comparison (Assignments vs Exams)", performance_comparison)
        row = write_table(row, 2, "🚨 At-Risk Students", at_risk)
        row = write_table(row, 2, "🌟 Top Performing Students", top)

        # ✅ Auto-fit columns
        for col_idx in range(1, ws.max_column + 1):
            max_len = 0
            for cell in ws[get_column_letter(col_idx)]:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
            ws.column_dimensions[get_column_letter(col_idx)].width = max_len + 3

        with BytesIO() as b:
            wb.save(b)
            return b.getvalue()

    # === CSV Export ===
    elif file_type == "csv":
        with BytesIO() as b:
            def write_section(title, df_table):
                b.write((title + "\n").encode())
                df_table.to_csv(b, index=False)
                b.write(b"\n\n")

            write_section("📊 Average Grade per Course", avg_grades)
            write_section("📉 Average Attendance per Course", avg_attendance)
            write_section("📈 Grade Distribution by Course", grade_dist)
            write_section("📋 Performance Comparison", performance_comparison)
            write_section("🚨 At-Risk Students", at_risk)
            write_section("🌟 Top Performing Students", top)

            return b.getvalue()

    return None

@app.route('/download_excel_students_overview_dashboard')
@login_required
def download_excel_students_overview_dashboard():
    excel_data = generate_students_overview_report("xlsx")
    return send_file(
        BytesIO(excel_data),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Students_Overview_Report.xlsx'
    )

@app.route('/download_csv_students_overview_dashboard')
@login_required
def download_csv_students_overview_dashboard():
    csv_data = generate_students_overview_report("csv")
    return send_file(
        BytesIO(csv_data),
        mimetype='text/csv',
        as_attachment=True,
        download_name='Students_Overview_Report.csv'
    )



import os
import json
import random
import pandas as pd
import openpyxl
from io import BytesIO, StringIO
from openpyxl.styles import Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def generate_student_attendance_insights_report(file_type="xlsx"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    def load_students(file_name):
        try:
            with open(os.path.join(DATA_DIR, file_name), "r", encoding="utf-8") as f:
                data = json.load(f)
            flat = []
            for entry in data:
                if isinstance(entry, list):
                    flat.extend(entry)
                elif isinstance(entry, dict):
                    flat.append(entry)
            return [(s["ID"], s["Student"], s["Attendance"]) for s in flat if "ID" in s and "Student" in s and "Attendance" in s]
        except:
            return []

    se_students = load_students("software_engineering.json")
    ds_students = load_students("data_science.json")

    if not se_students or not ds_students:
        return None

    se_lectures = [
        "Application Software", "Databases", "Operating Systems", "Networking",
        "Cybersecurity", "Cloud Computing", "Software Testing", "Artificial Intelligence",
        "Machine Learning", "Web Development", "Mobile Development", "DevOps"
    ]
    ds_lectures = [
        "Data Wrangling", "Big Data", "Data Visualization", "Statistics",
        "Machine Learning", "Deep Learning", "NLP", "AI Ethics",
        "Reinforcement Learning", "Cloud Computing for AI", "Model Deployment", "Data Science Projects"
    ]

    def simulate_attendance(students, lectures):
        week_labels = [f"Week {i+1} ({topic})" for i, topic in enumerate(lectures)]
        total_weeks = len(week_labels)
        data = []

        for student_id, name, overall_attendance in students:
            attended_count = round((overall_attendance / 100) * total_weeks)
            attended_weeks = sorted(random.sample(range(total_weeks), attended_count))
            weekly = [100 if i in attended_weeks else 0 for i in range(total_weeks)]
            data.append([student_id, name] + weekly)

        columns = ["Student ID", "Student Name"] + week_labels
        return pd.DataFrame(data, columns=columns)

    df_se = simulate_attendance(se_students, se_lectures)
    df_ds = simulate_attendance(ds_students, ds_lectures)

    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws_se = wb.active
        ws_se.title = "Software Engineering"
        ws_ds = wb.create_sheet("Data Science")

        def write_to_sheet(ws, df):
            header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
            border = Border(left=Side(style='thin'), right=Side(style='thin'),
                            top=Side(style='thin'), bottom=Side(style='thin'))

            for col_idx, col_name in enumerate(df.columns, start=1):
                cell = ws.cell(row=1, column=col_idx, value=col_name)
                cell.fill = header_fill
                cell.font = Font(bold=True)
                cell.border = border

            for row_idx, row_data in enumerate(df.itertuples(index=False), start=2):
                for col_idx, value in enumerate(row_data, start=1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    cell.border = border

                    # Attendance fill colors
                    if isinstance(value, (int, float)):
                        if value == 100:
                            cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # Green
                        elif value == 0:
                            cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")  # Red

            for col in ws.columns:
                max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
                ws.column_dimensions[col[0].column_letter].width = max_length + 2

        write_to_sheet(ws_se, df_se)
        write_to_sheet(ws_ds, df_ds)

        b = BytesIO()
        wb.save(b)
        b.seek(0)
        return b.getvalue()

    elif file_type == "csv":
        output = StringIO()
        output.write("Software Engineering\n")
        df_se.to_csv(output, index=False)
        output.write("\n\nData Science\n")
        df_ds.to_csv(output, index=False)
        return output.getvalue().encode("utf-8")

    return None


@app.route("/download_excel_student_attendance_insights_renamed")
def download_excel_student_attendance_insights_renamed():
    content = generate_student_attendance_insights_report("xlsx")
    if not content:
        return "❌ Export failed", 500

    return send_file(
        BytesIO(content),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        download_name="student_attendance_insights.xlsx",
        as_attachment=True
    )



@app.route("/download_csv_student_attendance_insights_renamed")
def download_csv_student_attendance_insights_renamed():
    content = generate_student_attendance_insights_report("csv")
    if not content:
        return "❌ CSV export failed", 500

    return send_file(
        BytesIO(content),
        mimetype="text/csv",
        download_name="student_attendance_insights.csv",
        as_attachment=True
    )





#✅ Function to generate Course Registers Export
def generate_course_registers_report(file_type="xlsx"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(BASE_DIR, "course_registers.json")  # ✅ your main folder

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Could not load course_registers.json: {e}")
        return None

    if not data or not isinstance(data, list):
        print("❌ Invalid or empty JSON content")
        return None

    df = pd.DataFrame(data)

    # Split students by course based on UNI ID prefix
    df_se = df[df["UNI ID"].str.startswith("SE")]
    df_ds = df[df["UNI ID"].str.startswith("DS")]

    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws_se = wb.active
        ws_se.title = "Software Engineering"
        ws_ds = wb.create_sheet("Data Science")

        def write_sheet(ws, df_course):
            header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
            border = Border(left=Side(style="thin"), right=Side(style="thin"),
                            top=Side(style="thin"), bottom=Side(style="thin"))

            columns = ["UNI ID", "NAME", "Role"]
            for col_num, header in enumerate(columns, start=1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.fill = header_fill
                cell.font = Font(bold=True)
                cell.border = border

            for row_idx, row in enumerate(df_course[columns].itertuples(index=False), start=2):
                for col_idx, value in enumerate(row, start=1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    cell.border = border

            for col in ws.columns:
                max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
                ws.column_dimensions[col[0].column_letter].width = max_len + 2

        write_sheet(ws_se, df_se)
        write_sheet(ws_ds, df_ds)

        b = BytesIO()
        wb.save(b)
        b.seek(0)
        return b.getvalue()

    elif file_type == "csv":
        output = StringIO()
        output.write("Software Engineering\n")
        df_se.to_csv(output, index=False)
        output.write("\n\nData Science\n")
        df_ds.to_csv(output, index=False)
        return output.getvalue().encode("utf-8")

    return None

@app.route("/download_excel_course_registers")
@login_required
def download_excel_course_registers():
    content = generate_course_registers_report("xlsx")
    if not content:
        return "❌ Excel export failed", 500
    return send_file(
        BytesIO(content),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        download_name="Course_Registers.xlsx",
        as_attachment=True
    )

@app.route("/download_csv_course_registers")
@login_required
def download_csv_course_registers():
    content = generate_course_registers_report("csv")
    if not content:
        return "❌ CSV export failed", 500
    return send_file(
        BytesIO(content),
        mimetype="text/csv",
        download_name="Course_Registers.csv",
        as_attachment=True
    )

## for admin course management
# ====================
# Database Connection
# ====================
def get_db_connection():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    return conn

# ====================
# API: Fetch All Courses
# ====================
@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return jsonify([dict(course) for course in courses])

# ====================
# Route: Course Management Page
# ====================
@app.route('/course_management')
def course_management():
    return render_template('course_management.html')

# ====================
# API: Fetch all students in a course
# ====================
@app.route('/api/course/<int:course_id>/students', methods=['GET'])
def get_course_students(course_id):
    conn = get_db_connection()
    students = conn.execute('''
        SELECT s.* FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = ?
    ''', (course_id,)).fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])

# ====================
# Route: View Course Page (students with 'Removed' status hidden)
# ====================
@app.route('/course/<int:course_id>/view')
def view_course(course_id):
    conn = get_db_connection()

    # Fetch course details
    course = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    if not course:
        conn.close()
        return "Course Not Found", 404

    # Fetch active enrolled users
    users_in_course = conn.execute('''
        SELECT s.* FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = ? AND s.enrollment_status != 'Removed'
        ORDER BY 
            CASE s.role
                WHEN 'Student' THEN 1
                WHEN 'Lecturer' THEN 2
                WHEN 'Teacher Assistant' THEN 3
                WHEN 'Admin' THEN 4
                ELSE 5
            END,
            s.join_date DESC
    ''', (course_id,)).fetchall()

    conn.close()

    course = dict(course)
    users = [dict(user) for user in users_in_course]

    # Template selection based on course name
    if "Software" in course["name"]:
        template = 'view_software.html'
    elif "Data Science" in course["name"]:
        template = 'view_data_science.html'
    else:
        template = 'view_generic.html'

    return render_template(template, course=course, users=users)

# ====================
# Route: Edit Course Page (Admin view)
# ====================
@app.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        students = request.form['students']
        lecturers = request.form['lecturers']
        status = request.form['status']

        conn.execute('''
            UPDATE courses
            SET name = ?, code = ?, students = ?, lecturers = ?, status = ?
            WHERE id = ?
        ''', (name, code, students, lecturers, status, course_id))
        conn.commit()
        conn.close()

        return redirect(url_for('edit_course', course_id=course_id, success='Course updated successfully!'))

    # Fetch course and all users (including 'Removed' for admin control)
    course = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()

    users_in_course = conn.execute('''
        SELECT s.* FROM students s
        JOIN enrollments e ON s.id = e.student_id
        WHERE e.course_id = ?
        ORDER BY 
            CASE s.role
                WHEN 'Student' THEN 1
                WHEN 'Lecturer' THEN 2
                WHEN 'Teacher Assistant' THEN 3
                WHEN 'Admin' THEN 4
                ELSE 5
            END,
            s.join_date DESC
    ''', (course_id,)).fetchall()

    conn.close()

    if not course:
        return "Course Not Found", 404

    course = dict(course)
    users = [dict(user) for user in users_in_course]

    if "Software" in course["name"]:
        template = 'edit_software.html'
    elif "Data Science" in course["name"]:
        template = 'edit_data_science.html'
    else:
        template = 'edit_generic.html'

    return render_template(template, course=course, users=users, success=request.args.get('success'))

# ====================
# Route: Add New User to Course
# ====================
@app.route('/course/<int:course_id>/add_user', methods=['POST'])
def add_user(course_id):
    name = request.form['name']
    role = request.form['role']
    enrollment_status = request.form['enrollment_status']
    course_name = request.form['course_name']
    join_date = datetime.now().strftime('%Y-%m-%d')

    initials = ''.join([part[0] for part in name.split()]).upper()
    random_number = random.randint(100000, 999999)

    if role == 'Student':
        uni_id = f"SE{random_number}" if "Software" in course_name else f"DS{random_number}"
        email = f"{initials}{uni_id}@uni.com"
    else:
        uni_id = str(random_number)
        email = f"{name.replace(' ', '').lower()}@uni.com"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO students (uni_id, username, email, role, join_date, enrollment_status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (uni_id, name, email, role, join_date, enrollment_status))

    student_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO enrollments (student_id, course_id)
        VALUES (?, ?)
    ''', (student_id, course_id))

    conn.commit()
    conn.close()

    return redirect(url_for('edit_course', course_id=course_id, success='Person added successfully!'))

# ====================
# Route: Archive (Soft Delete) User
# ====================
@app.route('/course/<int:course_id>/delete_user/<int:user_id>', methods=['POST'])
def delete_user(course_id, user_id):
    conn = get_db_connection()
    conn.execute('''
        UPDATE students
        SET enrollment_status = 'Removed'
        WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('edit_course', course_id=course_id, success='User archived successfully!'))

# ====================
# Route: Restore Archived User
# ====================
@app.route('/course/<int:course_id>/restore_user/<int:user_id>', methods=['POST'])
def restore_user(course_id, user_id):
    original_status = request.form.get('original_status', 'Active')

    conn = get_db_connection()
    conn.execute('''
        UPDATE students
        SET enrollment_status = ?
        WHERE id = ?
    ''', (original_status, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('edit_course', course_id=course_id, success='User restored successfully!'))









# ✅ Import Dashboards AFTER app is created
from dashboard_student import init_dashboard as init_student_dashboard
from data_structures_dashboard import init_dashboard as init_dsa_dashboard
from dashboard_web_dev import init_dashboard as init_webdev_dashboard
from dashboard_ai import init_dashboard as init_ai_dashboard
from dashboard_db import init_dashboard as init_db_dashboard
from dashboard_cybersecurity import init_dashboard as init_cybersecurity_dashboard
from dashboard_attendance import init_dashboard as init_attendance_dashboard
# ✅ Import Lecturer Dashboard
from dashboard_lecturer import init_lecturer_dashboard
from software_engineering_dashboard import init_software_engineering_dashboard
from data_science_dashboard import init_data_science_dashboard
from students_overview import init_students_overview
from student_attendance_insights import student_attendance_insights, init_student_attendance_insights
from course_registers import init_course_registers
from dashboard_admin import init_admin_dashboard
from dash_course_dashboard import init_course_dashboard

# ✅ Initialize Dashboards (ONLY ONCE)
init_student_dashboard(app)
init_dsa_dashboard(app)
init_webdev_dashboard(app)
init_ai_dashboard(app)
init_db_dashboard(app)
init_cybersecurity_dashboard(app)
init_attendance_dashboard(app)
init_lecturer_dashboard(app)  
init_software_engineering_dashboard(app)
init_data_science_dashboard(app)
init_students_overview(app)
app.register_blueprint(student_attendance_insights)
init_student_attendance_insights(app)
init_course_registers(app)
init_admin_dashboard(app)
init_course_dashboard(app)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
