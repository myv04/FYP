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

# ✅ Export Attendance Report
@app.route('/download_excel_attendance')
@login_required
def download_excel_attendance():
    data = {
        "Module": ["Data Structures", "Web Development", "AI", "Databases", "Cybersecurity"],
        "Attendance (%)": [75, 80, 85, 70, 65]
    }
    df = pd.DataFrame(data)
    return export_file(df, "attendance_report", "excel")

@app.route('/download_csv_attendance')
@login_required
def download_csv_attendance():
    data = {
        "Module": ["Data Structures", "Web Development", "AI", "Databases", "Cybersecurity"],
        "Attendance (%)": [75, 80, 85, 70, 65]
    }
    df = pd.DataFrame(data)
    return export_file(df, "attendance_report", "csv")

# Function to extract AI report data
def get_ai_data(file_type="excel"):
    file_path = f"ai_performance_report.{file_type}"

    # ✅ Updated Data
    module_title = ["MODULE: Artificial Intelligence"]
    module_code = ["Module Code: CS203"]

    average_attendance = 75
    completed_assignments = 1
    pending_assignments = 2
    current_grade = 25.50  # ✅ New addition

    metrics = [
        ["Average Attendance", average_attendance],
        ["Completed Assignments", completed_assignments],
        ["Pending Assignments", pending_assignments],
        ["Current Grade (%)", current_grade]  # ✅ Added Current Grade
    ]

    assignments = [
        ["ASSIGNMENT", "SCORE %"],  # ✅ Table Header
        ["Neural Network Implementation", 85],
        ["Ethical Concerns in AI Development", None],  # No score yet
        ["Sentiment Analysis using NLP", None]  # Not started
    ]

    # ✅ Excel Report Generation
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "AI Report"

        # ✅ Column Widths
        ws.column_dimensions["A"].width = 40
        ws.column_dimensions["B"].width = 20

        # ✅ Merged Header for Module Title
        ws.merge_cells("A1:B1")
        ws["A1"] = module_title[0]
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:B2")
        ws["A2"] = module_code[0]
        ws["A2"].alignment = Alignment(horizontal="center")

        # ✅ Attendance & Assignment Metrics (Bordered Table)
        start_row = 4
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                             top=Side(style='thin'), bottom=Side(style='thin'))
        for i, (metric, value) in enumerate(metrics):
            ws[f"A{start_row + i}"] = metric
            ws[f"B{start_row + i}"] = value
            ws[f"A{start_row + i}"].border = thin_border
            ws[f"B{start_row + i}"].border = thin_border

        # ✅ Assignment Scores Table
        ws["A8"] = "ASSIGNMENT"
        ws["B8"] = "SCORE %"
        ws["A8"].font = Font(bold=True)
        ws["B8"].font = Font(bold=True)

        start_row = 9
        for i, (assignment, score) in enumerate(assignments[1:]):
            ws[f"A{start_row + i}"] = assignment
            ws[f"B{start_row + i}"] = score if score is not None else ""

        # ✅ Add Excel Table with Filters
        table = Table(displayName="AssignmentScores", ref=f"A8:B{start_row + len(assignments) - 2}")
        style = TableStyleInfo(
            name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
            showRowStripes=True, showColumnStripes=False
        )
        table.tableStyleInfo = style
        ws.add_table(table)

        # ✅ Save File
        wb.save(file_path)
        return file_path

    # ✅ CSV Report Generation (Fixed to match old working version)
    elif file_type == "csv":
        with open(file_path, "w") as f:
            # ✅ Module Header
            f.write("MODULE: Artificial Intelligence\n")
            f.write("Module Code: CS203\n\n")

            # ✅ Metrics Table
            f.write("Metric,Value\n")
            for metric, value in metrics:
                f.write(f"{metric},{value}\n")

            f.write("\n")  # Space between tables

            # ✅ Assignment Table
            f.write("ASSIGNMENT,SCORE %\n")
            for assignment, score in assignments[1:]:
                f.write(f"{assignment},{score if score is not None else ''}\n")

        return file_path

# ✅ Routes for Downloading AI Report
@app.route('/download_excel_ai')
@login_required
def download_excel_ai():
    file_path = get_ai_data("xlsx")
    return send_file(file_path, as_attachment=True, download_name="AI_Report.xlsx")

@app.route('/download_csv_ai')
@login_required
def download_csv_ai():
    file_path = get_ai_data("csv")
    return send_file(file_path, as_attachment=True, download_name="AI_Report.csv")

# ✅ Export Web Development Report (Updated)
def get_webdev_data(file_type="excel"):
    file_path = f"webdev_performance_report.{file_type}"

    # ✅ Updated Data from New Web Dev Dashboard
    module_title = ["MODULE: Web Development"]
    module_code = ["Module Code: CS202"]

    # ✅ New Attendance & Assignment Metrics
    metrics = [
        ["Average Attendance", 80],
        ["Remaining Attendance", 20],  # New metric
        ["Completed Assignments", 1],  # Only 1 completed
        ["Pending Assignments", 0],  # No pending assignments
        ["Current Grade (%)", 79.0]  # New addition
    ]

    # ✅ New Assignment & Exam Scores (Matches Dashboard)
    assignments = [
        ["ASSESSMENT", "SCORE %"],  # Table Header
        ["Final Web Development Exam", 76],  # Updated Exam
        ["Responsive Design Project", 82]  # Updated Assignment
    ]

    # ✅ Excel Report Generation
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Web Dev Report"

        # ✅ Column Widths for Better Readability
        ws.column_dimensions["A"].width = 35
        ws.column_dimensions["B"].width = 15

        # ✅ 1. Merged Header for Module Title
        ws.merge_cells("A1:B1")
        ws["A1"] = module_title[0]
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:B2")
        ws["A2"] = module_code[0]
        ws["A2"].alignment = Alignment(horizontal="center")

        # ✅ 2. Attendance & Assignment Metrics Table
        start_row = 4
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                             top=Side(style='thin'), bottom=Side(style='thin'))
        for i, (metric, value) in enumerate(metrics):
            ws[f"A{start_row + i}"] = metric
            ws[f"B{start_row + i}"] = value
            ws[f"A{start_row + i}"].border = thin_border
            ws[f"B{start_row + i}"].border = thin_border

        # ✅ 3. Assignment & Exam Scores Table
        ws["A10"] = "ASSESSMENT"
        ws["B10"] = "SCORE %"
        ws["A10"].font = Font(bold=True)
        ws["B10"].font = Font(bold=True)

        start_row = 11
        for i, (assessment, score) in enumerate(assignments[1:]):
            ws[f"A{start_row + i}"] = assessment
            ws[f"B{start_row + i}"] = score

        # ✅ Add Excel Table with Filters
        table = Table(displayName="WebDevScores", ref=f"A10:B{start_row + len(assignments) - 2}")
        style = TableStyleInfo(
            name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
            showRowStripes=True, showColumnStripes=False
        )
        table.tableStyleInfo = style
        ws.add_table(table)

        # ✅ Save File
        wb.save(file_path)
        return file_path

    # ✅ CSV Report Generation (Updated Structure)
    elif file_type == "csv":
        with open(file_path, "w") as f:
            # ✅ Module Header
            f.write("MODULE: Web Development\n")
            f.write("Module Code: CS202\n\n")

            # ✅ Metrics Table
            f.write("Metric,Value\n")
            for metric, value in metrics:
                f.write(f"{metric},{value}\n")

            f.write("\n")  # Space between tables

            # ✅ Assignment & Exam Table
            f.write("ASSESSMENT,SCORE %\n")
            for assessment, score in assignments[1:]:
                f.write(f"{assessment},{score}\n")

        return file_path

# ✅ Routes for Downloading Updated Web Development Report
@app.route('/download_excel_webdev')
@login_required
def download_excel_webdev():
    file_path = get_webdev_data("xlsx")
    return send_file(file_path, as_attachment=True, download_name="WebDev_Report.xlsx")

@app.route('/download_csv_webdev')
@login_required
def download_csv_webdev():
    file_path = get_webdev_data("csv")
    return send_file(file_path, as_attachment=True, download_name="WebDev_Report.csv")

# Function to extract Database Management report data
def get_db_data(file_type="excel"):
    file_path = f"db_performance_report.{file_type}"

    # ✅ Updated Data
    module_title = ["MODULE: Database Management"]
    module_code = ["Module Code: CS203"]

    average_attendance = 82
    completed_assignments = 2
    pending_assignments = 1
    current_grade = 36.00  # ✅ Updated Current Grade

    metrics = [
        ["Average Attendance", average_attendance],
        ["Completed Assignments", completed_assignments],
        ["Pending Assignments", pending_assignments],
        ["Current Grade (%)", current_grade]  # ✅ Updated Current Grade
    ]

    assignments = [
        ["ASSESSMENT", "SCORE %"],  # ✅ Updated Table Header
        ["Normalization Techniques", 88],
        ["SQL Query Optimization", 92],
        ["Final Database Exam", "TBD"]
    ]

    # ✅ Excel Report Generation
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "DB Report"

        # ✅ Column Widths
        ws.column_dimensions["A"].width = 40
        ws.column_dimensions["B"].width = 20

        # ✅ Merged Header for Module Title
        ws.merge_cells("A1:B1")
        ws["A1"] = module_title[0]
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:B2")
        ws["A2"] = module_code[0]
        ws["A2"].alignment = Alignment(horizontal="center")

        # ✅ Attendance & Assignment Metrics (Bordered Table)
        start_row = 4
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                             top=Side(style='thin'), bottom=Side(style='thin'))
        for i, (metric, value) in enumerate(metrics):
            ws[f"A{start_row + i}"] = metric
            ws[f"B{start_row + i}"] = value
            ws[f"A{start_row + i}"].border = thin_border
            ws[f"B{start_row + i}"].border = thin_border

        # ✅ Assessment Scores Table
        ws["A8"] = "ASSESSMENT"  # ✅ Updated Header
        ws["B8"] = "SCORE %"
        ws["A8"].font = Font(bold=True)
        ws["B8"].font = Font(bold=True)

        start_row = 9
        for i, (assignment, score) in enumerate(assignments[1:]):
            ws[f"A{start_row + i}"] = assignment
            ws[f"B{start_row + i}"] = score if score != "TBD" else "Pending"

        # ✅ Add Excel Table with Filters
        table = Table(displayName="AssessmentScores", ref=f"A8:B{start_row + len(assignments) - 2}")
        style = TableStyleInfo(
            name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
            showRowStripes=True, showColumnStripes=False
        )
        table.tableStyleInfo = style
        ws.add_table(table)

        # ✅ Save File
        wb.save(file_path)
        return file_path

    # ✅ CSV Report Generation
    elif file_type == "csv":
        with open(file_path, "w") as f:
            # ✅ Module Header
            f.write("MODULE: Database Management\n")
            f.write("Module Code: CS203\n\n")

            # ✅ Metrics Table
            f.write("Metric,Value\n")
            for metric, value in metrics:
                f.write(f"{metric},{value}\n")

            f.write("\n")  # Space between tables

            # ✅ Assessment Table
            f.write("ASSESSMENT,SCORE %\n")  # ✅ Updated Header
            for assignment, score in assignments[1:]:
                f.write(f"{assignment},{score if score != 'TBD' else 'Pending'}\n")

        return file_path

# ✅ Routes for Downloading DB Report
@app.route('/download_excel_db')
@login_required
def download_excel_db():
    file_path = get_db_data("xlsx")
    return send_file(file_path, as_attachment=True, download_name="DB_Report.xlsx")

@app.route('/download_csv_db')
@login_required
def download_csv_db():
    file_path = get_db_data("csv")
    return send_file(file_path, as_attachment=True, download_name="DB_Report.csv")


# ✅ Export Cybersecurity Report
# ✅ Function to generate Cybersecurity report for Excel & CSV
def get_cybersecurity_data(file_type="excel"):
    file_path = f"cybersecurity_performance_report.{file_type}"

    # ✅ Data for Cybersecurity Report
    module_title = ["MODULE: Cybersecurity"]
    module_code = ["Module Code: CS305"]

    metrics = [
        ["Average Attendance", 78],
        ["Completed Assignments", 2],
        ["Pending Assignments", 1],
        ["Current Grade (%)", 68.80]  # ✅ Updated Current Grade
    ]

    assignments = [
        ["ASSESSMENT", "SCORE %"],  # ✅ Updated Table Header
        ["Network Security Protocols", 95],
        ["Ethical Hacking Fundamentals", 88],
        ["Malware Analysis", None]  # Pending
    ]

    # ✅ Excel Report Generation
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Cybersecurity Report"

        # ✅ Column Widths
        ws.column_dimensions["A"].width = 35
        ws.column_dimensions["B"].width = 15

        # ✅ 1. Merged Header for Module Title
        ws.merge_cells("A1:B1")
        ws["A1"] = module_title[0]
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:B2")
        ws["A2"] = module_code[0]
        ws["A2"].alignment = Alignment(horizontal="center")

        # ✅ 2. Attendance & Assignment Metrics (Bordered Table)
        start_row = 4
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                             top=Side(style='thin'), bottom=Side(style='thin'))
        for i, (metric, value) in enumerate(metrics):
            ws[f"A{start_row + i}"] = metric
            ws[f"B{start_row + i}"] = value
            ws[f"A{start_row + i}"].border = thin_border
            ws[f"B{start_row + i}"].border = thin_border

        # ✅ 3. Assignment Scores Table with Filters
        ws["A8"] = "ASSESSMENT"
        ws["B8"] = "SCORE %"
        ws["A8"].font = Font(bold=True)
        ws["B8"].font = Font(bold=True)

        start_row = 9
        for i, (assignment, score) in enumerate(assignments[1:]):
            ws[f"A{start_row + i}"] = assignment
            ws[f"B{start_row + i}"] = score if score is not None else ""

        # ✅ Add Excel Table with Filters
        table = Table(displayName="CyberAssignments", ref=f"A8:B{start_row + len(assignments) - 2}")
        style = TableStyleInfo(
            name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
            showRowStripes=True, showColumnStripes=False
        )
        table.tableStyleInfo = style
        ws.add_table(table)

        # ✅ Save File
        wb.save(file_path)
        return file_path

    # ✅ CSV Report Generation (Same Structure)
    elif file_type == "csv":
        with open(file_path, "w") as f:
            # ✅ Module Header
            f.write("MODULE: Cybersecurity\n")
            f.write("Module Code: CS305\n\n")

            # ✅ Metrics Table
            f.write("Metric,Value\n")
            for metric, value in metrics:
                f.write(f"{metric},{value}\n")

            f.write("\n")  # Space between tables

            # ✅ Assignment Table
            f.write("ASSESSMENT,SCORE %\n")
            for assignment, score in assignments[1:]:
                f.write(f"{assignment},{score if score is not None else ''}\n")

        return file_path

# ✅ Routes for Downloading Cybersecurity Report
@app.route('/download_excel_cybersecurity')
@login_required
def download_excel_cybersecurity():
    file_path = get_cybersecurity_data("xlsx")
    return send_file(file_path, as_attachment=True, download_name="Cybersecurity_Report.xlsx")

@app.route('/download_csv_cybersecurity')
@login_required
def download_csv_cybersecurity():
    file_path = get_cybersecurity_data("csv")
    return send_file(file_path, as_attachment=True, download_name="Cybersecurity_Report.csv")
    
# ✅ Export Student Performance Report
# ✅ Function to generate Student Performance Dashboard report for Excel & CSV
# ✅ Function to generate Student Performance Dashboard report for Excel & CSV
def get_student_performance_data(file_type="excel"):
    file_path = f"student_performance_report.{file_type}"

    # ✅ Data for Student Performance Report
    student_name = "Student: Mohammed Vohra"
    student_id = "Student ID: 210034354"
    attendance = "65%"

    grades = [
        ["CS201: Data Structure & Algorithm", 70],
        ["CS202: Web Development", 73],
        ["CS203: Artificial Intelligence", 25.5],
        ["CS204: Database Management", 36],
        ["CS205: Cybersecurity", 68.8]
    ]

    assignments = [
        ["CS202: Web Development", "Responsive Design Project", "82%", "Completed"],
        ["CS203: Artificial Intelligence", "Neural Network Implementation", "85%", "Completed"],
        ["CS203: Artificial Intelligence", "Ethical Concerns in AI Development", "n/a", "Not Completed"],
        ["CS203: Artificial Intelligence", "Sentiment Analysis using NLP", "n/a", "Not Started"],
        ["CS204: Database Management", "Normalization Techniques", "88%", "Completed"],
        ["CS204: Database Management", "SQL Query Optimization", "92%", "Completed"],
        ["CS205: Cybersecurity", "Network Security Protocols", "80%", "Completed"],
        ["CS205: Cybersecurity", "Ethical Hacking Fundamentals", "68%", "Completed"],
        ["CS205: Cybersecurity", "Malware Analysis", "n/a", "Not Started"]
    ]

    exams = [
        ["CS201: Data Structure & Algorithm", "DSA Exam", "78%", "Completed"],
        ["CS202: Web Development", "Web Dev Exam", "85%", "Completed"],
        ["CS204: Database Management", "Ethical Concerns in AI Development", "n/a", "Not Completed"]
    ]

    deadlines = [
        ["CS203: Artificial Intelligence", "Ethical Concerns in AI Development", "21/03/2025", "10"],
        ["CS202: Web Development", "Sentiment Analysis using NLP", "TBC", "TBC"],
        ["CS204: Database Management", "Malware Analysis", "TBC", "TBC"]
    ]

    # ✅ Generate Excel Report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Student Performance Report"

        # ✅ Formatting styles
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")  # Gold
        completed_fill = PatternFill(start_color="92D050", end_color="92D050", fill_type="solid")  # Green
        not_completed_fill = PatternFill(start_color="FF5050", end_color="FF5050", fill_type="solid")  # Red
        border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                        top=Side(style='thin'), bottom=Side(style='thin'))

        # ✅ Title (Merged)
        ws.merge_cells("A1:D1")
        ws["A1"] = "STUDENT PERFORMANCE DASHBOARD"
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:D2")
        ws["A2"] = student_name
        ws["A2"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A3:D3")
        ws["A3"] = student_id
        ws["A3"].alignment = Alignment(horizontal="center")

        ws["A5"] = "Average attendance for the year"
        ws["B5"] = attendance

        # ✅ Grades Section
        ws.merge_cells("A7:D7")
        ws["A7"] = "Percentage of grades per module so far"
        ws["A7"].fill = header_fill
        ws["A7"].alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Grade %"])
        for row in grades:
            ws.append(row)

        # Apply borders to grades table
        for row in ws.iter_rows(min_row=9, max_row=9 + len(grades), min_col=1, max_col=2):
            for cell in row:
                cell.border = border

        # ✅ Assignments Section
        ws.append([""])  # Empty row for spacing
        ws.merge_cells("A14:D14")
        ws["A14"] = "Assignments completion status by Module"
        ws["A14"].fill = header_fill
        ws["A14"].alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Assignment Name", "Score", "Status"])
        for row in assignments:
            ws.append(row)

        # Apply borders and coloring for assignments table
        for row in ws.iter_rows(min_row=16, max_row=16 + len(assignments), min_col=1, max_col=4):
            for cell in row:
                cell.border = border
                if cell.column == 4:  # Status column
                    if cell.value == "Completed":
                        cell.fill = completed_fill
                    elif cell.value in ["Not Completed", "Not Started"]:
                        cell.fill = not_completed_fill

        # ✅ Exams Section
        ws.append([""])  # Empty row for spacing
        ws.merge_cells("A26:D26")
        ws["A26"] = "Exam completion status by Module"
        ws["A26"].fill = header_fill
        ws["A26"].alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Exam Name", "Score", "Status"])
        for row in exams:
            ws.append(row)

        # Apply borders for exams table
        for row in ws.iter_rows(min_row=28, max_row=28 + len(exams), min_col=1, max_col=4):
            for cell in row:
                cell.border = border
                if cell.column == 4 and cell.value == "Not Completed":
                    cell.fill = not_completed_fill

        # ✅ Deadlines Section
        ws.append([""])  # Empty row for spacing
        ws.merge_cells("A32:D32")
        ws["A32"] = "Upcoming Deadlines"
        ws["A32"].fill = header_fill
        ws["A32"].alignment = Alignment(horizontal="center")

        ws.append(["Module Name", "Assignment Name", "Deadline Date", "Days Left"])
        for row in deadlines:
            ws.append(row)

        # Apply borders for deadlines table
        for row in ws.iter_rows(min_row=34, max_row=34 + len(deadlines), min_col=1, max_col=4):
            for cell in row:
                cell.border = border

        # ✅ Save Excel File
        wb.save(file_path)
        return file_path

    # ✅ Generate CSV Report
    elif file_type == "csv":
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            f.write("STUDENT PERFORMANCE DASHBOARD\n")
            f.write(f"{student_name}\n")
            f.write(f"{student_id}\n\n")

            f.write("Average Attendance,65%\n\n")

            f.write("Module Name,Grade %\n")
            for row in grades:
                f.write(",".join(map(str, row)) + "\n")
            f.write("\n")

            f.write("Module Name,Assignment Name,Score,Status\n")
            for row in assignments:
                f.write(",".join(map(str, row)) + "\n")
            f.write("\n")

            f.write("Module Name,Exam Name,Score,Status\n")
            for row in exams:
                f.write(",".join(map(str, row)) + "\n")
            f.write("\n")

            f.write("Module Name,Assignment Name,Deadline Date,Days Left\n")
            for row in deadlines:
                f.write(",".join(map(str, row)) + "\n")

        return file_path

    return None  # If file_type is invalid

# ✅ Flask Routes
@app.route('/download_excel_student_performance')
def download_excel_student_performance():
    file_path = get_student_performance_data("xlsx")
    return send_file(file_path, as_attachment=True, download_name="Student_Performance_Report.xlsx")

@app.route('/download_csv_student_performance')
def download_csv_student_performance():
    file_path = get_student_performance_data("csv")
    return send_file(file_path, as_attachment=True, download_name="Student_Performance_Report.csv")
# ✅ Export Data Structures Report
# ✅ Function to generate Data Structures & Algorithms report for Excel & CSV
def get_dsa_data(file_type="excel"):
    file_path = f"dsa_performance_report.{file_type}"

    # ✅ Data for DSA Report
    module_title = ["MODULE: Data Structures & Algorithms"]
    module_code = ["Module Code: CS201"]

    metrics = [
        ["Average Attendance", 85],
        ["Current Grade", "78%"]
    ]

    exam_details = [
        ["ASSESSMENT", "SCORE %"],  # Table Header
        ["DSA Exam", 78]
    ]

    # ✅ Excel Report Generation
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "DSA Report"

        # ✅ Column Widths
        ws.column_dimensions["A"].width = 35
        ws.column_dimensions["B"].width = 15

        # ✅ 1. Merged Header for Module Title
        ws.merge_cells("A1:B1")
        ws["A1"] = module_title[0]
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells("A2:B2")
        ws["A2"] = module_code[0]
        ws["A2"].alignment = Alignment(horizontal="center")

        # ✅ 2. Attendance & Grade Metrics
        start_row = 4
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                             top=Side(style='thin'), bottom=Side(style='thin'))
        for i, (metric, value) in enumerate(metrics):
            ws[f"A{start_row + i}"] = metric
            ws[f"B{start_row + i}"] = value
            ws[f"A{start_row + i}"].border = thin_border
            ws[f"B{start_row + i}"].border = thin_border

        # ✅ 3. Exam Score Table
        ws["A7"] = "ASSESSMENT"
        ws["B7"] = "SCORE %"
        ws["A7"].font = Font(bold=True)
        ws["B7"].font = Font(bold=True)

        start_row = 8
        for i, (exam, score) in enumerate(exam_details[1:]):
            ws[f"A{start_row + i}"] = exam
            ws[f"B{start_row + i}"] = score

        # ✅ Add Excel Table with Filters
        table = Table(displayName="DSAExam", ref=f"A7:B{start_row + len(exam_details) - 2}")
        style = TableStyleInfo(
            name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
            showRowStripes=True, showColumnStripes=False
        )
        table.tableStyleInfo = style
        ws.add_table(table)

        # ✅ Save File
        wb.save(file_path)
        return file_path

    # ✅ CSV Report Generation (Same Structure)
    elif file_type == "csv":
        with open(file_path, "w") as f:
            # ✅ Module Header
            f.write("MODULE: Data Structures & Algorithms\n")
            f.write("Module Code: CS201\n\n")

            # ✅ Metrics Table
            f.write("Metric,Value\n")
            for metric, value in metrics:
                f.write(f"{metric},{value}\n")

            f.write("\n")  # Space between tables

            # ✅ Exam Table
            f.write("ASSESSMENT,SCORE %\n")
            for exam, score in exam_details[1:]:
                f.write(f"{exam},{score}\n")

        return file_path

# ✅ Routes for Downloading DSA Report
@app.route('/download_excel_dsa')
@login_required
def download_excel_dsa():
    file_path = get_dsa_data("xlsx")
    return send_file(file_path, as_attachment=True, download_name="DSA_Report.xlsx")

@app.route('/download_csv_dsa')
@login_required
def download_csv_dsa():
    file_path = get_dsa_data("csv")
    return send_file(file_path, as_attachment=True, download_name="DSA_Report.csv")

# lecturers expots
# ✅ Function to generate Lecturer Dashboard Export with updated data
def generate_lecturer_dashboard_report(file_type="excel"):
    file_path = f"overview_dashboard.{file_type}"

    # 📌 Updated Data from Lecturer Dashboard
    metrics = [
        ["Metric", "Value"],
        ["Average Attendance (%)", 85],
        ["Remaining Attendance (%)", 15],
        ["Software Engineering Avg Score (%)", 82],
        ["Data Science Avg Score (%)", 88]
    ]

    assignments = [
        ["Assignment", "Completed", "Completed with Penalty", "Not Completed", "Absent"],
        ["Agile Development - Assignment 1 (Bugs and Fixes)", 42, 3, 3, 2],
        ["Agile Development - Assignment 2 (Software Architecture)", 37, 8, 4, 1],
        ["Machine Learning - Assignment 1 (Data Analysis)", 40, 8, 2, 0],
        ["Machine Learning - Assignment 2 (Machine Learning)", 42, 5, 3, 0]
    ]

    # ✅ Generate Excel Report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Lecturer Overview Report"

        # ✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                        top=Side(style='thin'), bottom=Side(style='thin'))

        # ✅ Metrics Table
        ws.merge_cells("A1:B1")
        ws["A1"] = "Lecturer Dashboard Overview"
        ws["A1"].font = Font(bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        for row_idx, row in enumerate(metrics, start=3):
            ws.append(row)
            ws[f"A{row_idx}"].border = border
            ws[f"B{row_idx}"].border = border
            if row_idx == 3:
                ws[f"A{row_idx}"].fill = header_fill
                ws[f"B{row_idx}"].fill = header_fill

        # ✅ Assignments Table
        ws.append([""])  # Empty row for spacing
        start_row = len(metrics) + 5
        for row_idx, row in enumerate(assignments, start=start_row):
            ws.append(row)
            for col in range(1, len(row) + 1):
                cell = ws.cell(row=row_idx, column=col)
                cell.border = border
                if row_idx == start_row:
                    cell.fill = header_fill

        # ✅ Save Excel File
        wb.save(file_path)
        return file_path

    # ✅ Generate CSV Report
    elif file_type == "csv":
        df_metrics = pd.DataFrame(metrics[1:], columns=metrics[0])
        df_assignments = pd.DataFrame(assignments[1:], columns=assignments[0])

        with open(file_path, "w") as f:
            df_metrics.to_csv(f, index=False)
            f.write("\n")  # Add a blank line between tables
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

    # 📌 Sample Data from Software Engineering Dashboard
    student_names = [
        "Alice Johnson", "Bob Smith", "Charlie Davis", "David Martinez", "Eve Brown",
        "Frank Wilson", "Grace Taylor", "Hank Anderson", "Ivy Thomas", "Jack White",
        "Karen Harris", "Leo Martin", "Mona Clark", "Nathan Lewis", "Olivia Hall",
        "Peter Allen", "Quincy Young", "Rachel King", "Steve Wright", "Tina Scott",
        "Uma Green", "Victor Adams", "Wendy Baker", "Xander Nelson", "Yvonne Carter",
        "Zachary Mitchell", "Aaron Perez", "Bella Roberts", "Cody Gonzalez", "Diana Campbell",
        "Ethan Rodriguez", "Fiona Moore", "George Edwards", "Holly Flores", "Ian Cooper",
        "Julia Murphy", "Kevin Reed", "Laura Cox", "Mike Ward", "Nina Peterson",
        "Oscar Gray", "Paula Jenkins", "Quinn Russell", "Randy Torres", "Samantha Stevens",
        "Tommy Parker", "Ursula Evans", "Vince Morgan", "Whitney Bell", "Xavier Phillips"
    ]

    student_ids = [f"SE{random.randint(1000,9999)}" for _ in student_names]
    attendance_scores = [random.randint(70, 100) if random.random() > 0.1 else random.randint(50, 69) for _ in student_names]

    assignment_1_status = ["Completed"] * 45 + ["Absent"] * 2 + ["Not Completed"] * 3
    random.shuffle(assignment_1_status)
    assignment_2_status = ["Completed"] * 45 + ["Absent"] * 2 + ["Not Completed"] * 3
    random.shuffle(assignment_2_status)

    assignment_1_scores = [random.randint(65, 98) if status == "Completed" else 0 for status in assignment_1_status]
    assignment_2_scores = [random.randint(65, 98) if status == "Completed" else 0 for status in assignment_2_status]

    # Ensure students with 0 score on one assignment still have scores on the other
    for i in range(len(student_names)):
        if assignment_1_scores[i] == 0 and assignment_2_scores[i] == 0:
            if random.choice([True, False]):
                assignment_1_scores[i] = random.randint(65, 98)
                assignment_1_status[i] = "Completed"
            else:
                assignment_2_scores[i] = random.randint(65, 98)
                assignment_2_status[i] = "Completed"

    exam_status = ["Fit to Sit" if random.random() > 0.05 else "Absent" for _ in student_names]
    exam_scores = [random.randint(55, 95) if status == "Fit to Sit" else 0 for status in exam_status]

    students_with_penalties = random.sample(range(len(student_names)), min(8, len(student_names)))  
    students_with_word_count = random.sample([i for i in range(len(student_names)) if i not in students_with_penalties], 3)

    penalty_flags_1 = ["" for _ in student_names]
    penalty_flags_2 = ["" for _ in student_names]

    for i in students_with_penalties:
        penalty_type = random.choice(["🚩 Academic Misconduct", "🚩 Exceptional Circumstances", "🚩 Lateness Penalty (-5%)"])
        if random.random() < 0.5:  
            penalty_flags_1[i] = penalty_type  
        else:
            penalty_flags_2[i] = penalty_type  

    for i in students_with_word_count:
        if penalty_flags_1[i] == "" and penalty_flags_2[i] == "":
            if random.random() < 0.5:
                penalty_flags_1[i] = "🚩 Word Count Penalty (-10%)"
            else:
                penalty_flags_2[i] = "🚩 Word Count Penalty (-10%)"

    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.25) + (a2 * 0.25) + (exam * 0.5)

        if p1 == '🚩 Lateness Penalty (-5%)' or p2 == '🚩 Lateness Penalty (-5%)':
            grade *= 0.95

        if p1 == '🚩 Word Count Penalty (-10%)' or p2 == '🚩 Word Count Penalty (-10%)':
            grade *= 0.9

        return round(grade, 2)

    final_grades = [calculate_final_grade(a1, a2, exam, p1, p2) 
                    for a1, a2, exam, p1, p2 in zip(assignment_1_scores, assignment_2_scores,
                                                    exam_scores, penalty_flags_1, penalty_flags_2)]

    statuses = ["Enrolled"] * 45 + ["Deferred"] * 3 + ["Dropped"] * 2
    random.shuffle(statuses)

    df = pd.DataFrame({
        "ID": student_ids,
        "Student": student_names,
        "Final Grade": final_grades,
        "Attendance (%)": attendance_scores,
        "Exam Status": exam_status,
        "Exam Score": exam_scores,
        "Assignment 1 (Bugs and Fixes)": assignment_1_scores,
        "Assignment 1 Status": assignment_1_status,
        "Assignment 1 Penalty": penalty_flags_1,
        "Assignment 2 (Software Architecture)": assignment_2_scores,
        "Assignment 2 Status": assignment_2_status,
        "Assignment 2 Penalty": penalty_flags_2,
        "Status": statuses
    })

    # ✅ Generate Excel Report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Software Engineering Report"

        # ✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                        top=Side(style='thin'), bottom=Side(style='thin'))

        ws.append(df.columns.tolist())

        #✅ Apply styling to headers
        for col_num, column_title in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_num, value=column_title)
            cell.fill = header_fill
            cell.border = border

        #✅ Insert data
        for row in df.itertuples(index=False):
            ws.append(list(row))

        # Prepare the Excel file for download
        with BytesIO() as b:
            wb.save(b)
            return b.getvalue()

    #✅ Generate CSV Report
    elif file_type == "csv":
        csv_data = df.to_csv(index=False)
        return csv_data.encode('utf-8')

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

    # 📌 Sample Data from Data Science Dashboard
    student_names = [
        "Alex Carter", "Bella Sanders", "Cameron Hughes", "Diana Wright", "Ethan Parker",
        "Felicity James", "Gabriel Lewis", "Hannah Stone", "Ian Turner", "Jasmine Collins",
        "Kevin Morris", "Lara Watson", "Michael Griffin", "Natalie Cooper", "Owen Richardson",
        "Paige Scott", "Quentin Ramirez", "Rebecca Bennett", "Stephen Howard", "Tracy Bell",
        "Ulysses Barnes", "Victoria Foster", "Walter Henderson", "Xander Nelson", "Yvette Campbell",
        "Zane Mitchell", "Amelia Ross", "Benjamin Ward", "Chloe Edwards", "David Fisher",
        "Emma Butler", "Frederick Murphy", "Grace Price", "Henry Stewart", "Isabella Torres",
        "Jackie Peterson", "Kurt Bailey", "Lucy Jenkins", "Mason Cooper", "Nina Adams",
        "Oscar Flores", "Penelope Russell", "Ryan Powell", "Sophia Simmons", "Theodore White",
        "Ursula Martin", "Vince Brown", "William Gonzales", "Xenia Moore", "Zoe Walker"
    ]

    student_ids = [f"DS{random.randint(1000,9999)}" for _ in student_names]
    attendance_scores = [random.randint(55, 100) if random.random() > 0.1 else random.randint(30, 49) for _ in student_names]

    assignment_1_status = ["Completed"] * 48 + ["Not Completed"] * 2
    random.shuffle(assignment_1_status)
    assignment_2_status = ["Completed"] * 48 + ["Not Completed"] * 2
    random.shuffle(assignment_2_status)

    assignment_1_scores = [random.randint(50, 95) if status == "Completed" else 0 for status in assignment_1_status]
    assignment_2_scores = [random.randint(50, 95) if status == "Completed" else 0 for status in assignment_2_status]

    penalty_flags_1 = ["🚩 Academic Misconduct" if random.random() < 0.05 else
                       "🚩 Exceptional Circumstances" if random.random() < 0.05 else
                       "🚩 Lateness Penalty (-5%)" if random.random() < 0.1 else "" for _ in student_names]

    penalty_flags_2 = ["🚩 Academic Misconduct" if random.random() < 0.05 else
                       "🚩 Exceptional Circumstances" if random.random() < 0.05 else
                       "🚩 Lateness Penalty (-5%)" if random.random() < 0.1 else "" for _ in student_names]

    exam_status = ["Fit to Sit" if random.random() > 0.05 else "Absent" for _ in student_names]
    exam_scores = [random.randint(50, 95) if status == "Fit to Sit" else 0 for status in exam_status]

    def calculate_final_grade(a1, a2, exam, p1, p2):
        grade = (a1 * 0.4) + (a2 * 0.3) + (exam * 0.3)
        
        if "Lateness Penalty" in p1:
            grade -= a1 * 0.4 * 0.05
        if "Lateness Penalty" in p2:
            grade -= a2 * 0.3 * 0.05
        
        return round(max(grade, 0), 2)

    final_grades = [calculate_final_grade(a1, a2, exam, p1, p2) 
                    for a1, a2, exam, p1, p2 in zip(assignment_1_scores, assignment_2_scores,
                                                    exam_scores, penalty_flags_1, penalty_flags_2)]

    statuses = ["Enrolled"] * 45 + ["Deferred"] * 3 + ["Dropped"] * 2
    random.shuffle(statuses)

    df = pd.DataFrame({
        "ID": student_ids,
        "Student": student_names,
        "Final Grade": final_grades,
        "Attendance (%)": attendance_scores,
        "Exam Status": exam_status,
        "Exam Score": exam_scores,
        "Assignment 1 (Data Analysis)": assignment_1_scores,
        "Assignment 1 Status": assignment_1_status,
        "Assignment 1 Penalty": penalty_flags_1,
        "Assignment 2 (Machine Learning)": assignment_2_scores,
        "Assignment 2 Status": assignment_2_status,
        "Assignment 2 Penalty": penalty_flags_2,
        "Status": statuses
    })

    # ✅ Generate Excel Report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data Science Report"

        # ✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                        top=Side(style='thin'), bottom=Side(style='thin'))

        ws.append(df.columns.tolist())

        # Apply styling to headers
        for col_num, column_title in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_num, value=column_title)
            cell.fill = header_fill
            cell.border = border

        # Insert data
        for row in df.itertuples(index=False):
            ws.append(list(row))

        # Prepare the Excel file for download
        with BytesIO() as b:
            wb.save(b)
            return b.getvalue()

    # ✅ Generate CSV Report
    elif file_type == "csv":
        csv_data = df.to_csv(index=False)
        return csv_data.encode('utf-8')

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
    file_path = f"students_overview_dashboard.{file_type}"  # ✅ Match working filenames

    # 📌 Sample Data from Students Overview Dashboard
    data = {
        "ID": [f"S{1000 + i}" for i in range(1, 21)],
        "Student": [f"Student {i}" for i in range(1, 21)],
        "Course": random.choices(["Software Engineering", "Data Science"], k=20),
        "Final Grade (%)": [random.randint(50, 100) for _ in range(20)],
        "Attendance (%)": [random.randint(60, 100) for _ in range(20)],
        "Assignment 1 Score": [random.randint(50, 95) for _ in range(20)],
        "Assignment 2 Score": [random.randint(50, 95) for _ in range(20)],
        "Exam Score": [random.randint(50, 100) for _ in range(20)],
        "Status": random.choices(["Enrolled", "Deferred", "Dropped"], k=20)
    }

    df = pd.DataFrame(data)

    # ✅ Generate Excel Report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students Overview Report"

        # ✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'),
                        top=Side(style='thin'), bottom=Side(style='thin'))

        ws.append(df.columns.tolist())

        # Apply styling to headers
        for col_num, column_title in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_num, value=column_title)
            cell.fill = header_fill
            cell.border = border

        # Insert data
        for row in df.itertuples(index=False):
            ws.append(list(row))

        # ✅ Save Excel File
        wb.save(file_path)
        return file_path

    # ✅ Generate CSV Report
    elif file_type == "csv":
        df.to_csv(file_path, index=False)
        return file_path

    return None  # If invalid file_type is provided

# ✅ Flask Routes to Export Students Overview Report
def generate_students_overview_report(file_type="excel"):
    # Sample data from the Students Overview Dashboard
    software_engineering_data = [
        ("Alice Johnson", 90.25), ("Bob Smith", 81.5), ("Charlie Davis", 77), ("David Martinez", 80.75),
        ("Eve Brown", 84.75), ("Frank Wilson", 72), ("Grace Taylor", 91), ("Hank Anderson", 73),
        ("Ivy Thomas", 93.25), ("Jack White", 76.5), ("Karen Harris", 68.5), ("Leo Martin", 84.75),
        ("Mona Clark", 76.5), ("Nathan Lewis", 63.25), ("Olivia Hall", 76), ("Peter Allen", 84),
        ("Quincy Young", 79.5), ("Rachel King", 91.5), ("Steve Wright", 85.5), ("Tina Scott", 74.75),
        ("Uma Green", 71.55), ("Victor Adams", 76), ("Wendy Baker", 91), ("Xander Nelson", 79),
        ("Yvonne Carter", 82.75), ("Zachary Mitchell", 75.6), ("Aaron Perez", 75.5), ("Bella Roberts", 81.25),
        ("Cody Gonzalez", 72.91), ("Diana Campbell", 76.25), ("Ethan Rodriguez", 88), ("Fiona Moore", 76.05),
        ("George Edwards", 78), ("Holly Flores", 77.75), ("Ian Cooper", 66), ("Julia Murphy", 70.25),
        ("Kevin Reed", 81.75), ("Laura Cox", 85.5), ("Mike Ward", 83.75), ("Nina Peterson", 70),
        ("Oscar Gray", 79.5), ("Paula Jenkins", 75.5), ("Quinn Russell", 81.5), ("Randy Torres", 92),
        ("Samantha Stevens", 75.75), ("Tommy Parker", 79.75), ("Ursula Evans", 32.3), ("Vince Morgan", 86),
        ("Whitney Bell", 74.25), ("Xavier Phillips", 70.5)
    ]

    data_science_data = [
        ("Alex Carter", 65.3), ("Bella Sanders", 70.77), ("Cameron Hughes", 55.62), ("Diana Wright", 77.9),
        ("Ethan Parker", 73.5), ("Felicity James", 67.7), ("Gabriel Lewis", 77.4), ("Hannah Stone", 60.1),
        ("Ian Turner", 71.19), ("Jasmine Collins", 61.6), ("Kevin Morris", 91.3), ("Lara Watson", 70.7),
        ("Michael Griffin", 71.9), ("Natalie Cooper", 56.8), ("Owen Richardson", 55.38), ("Paige Scott", 73.2),
        ("Quentin Ramirez", 47.7), ("Rebecca Bennett", 65.44), ("Stephen Howard", 76.28), ("Tracy Bell", 76.8),
        ("Ulysses Barnes", 68.3), ("Victoria Foster", 84.4), ("Walter Henderson", 72.8), ("Xander Nelson", 72.4),
        ("Yvette Campbell", 70.2), ("Zane Mitchell", 72.4), ("Amelia Ross", 68.2), ("Benjamin Ward", 64.03),
        ("Chloe Edwards", 72.9), ("David Fisher", 76.6), ("Emma Butler", 63.7), ("Frederick Murphy", 71.2),
        ("Grace Price", 77), ("Henry Stewart", 67.5), ("Isabella Torres", 79.9), ("Jackie Peterson", 79.4),
        ("Kurt Bailey", 65.6), ("Lucy Jenkins", 73.7), ("Mason Cooper", 46.5), ("Nina Adams", 73.5),
        ("Oscar Flores", 43.7), ("Penelope Russell", 91.4), ("Ryan Powell", 67.1), ("Sophia Simmons", 70.27),
        ("Theodore White", 67.7), ("Ursula Martin", 79.1), ("Vince Brown", 75.5), ("William Gonzales", 77.4),
        ("Xenia Moore", 71.3), ("Zoe Walker", 56.4)
    ]

    # Create DataFrames
    df_se = pd.DataFrame(software_engineering_data, columns=['Student', 'Grade'])
    df_se['Course'] = 'Software Engineering'
    df_ds = pd.DataFrame(data_science_data, columns=['Student', 'Grade'])
    df_ds['Course'] = 'Data Science'

    # Combine DataFrames
    df_combined = pd.concat([df_se, df_ds])

    # Calculate average grades and attendance
    avg_grades = df_combined.groupby('Course')['Grade'].mean().reset_index()
    avg_attendance = pd.DataFrame({
        "Course": ["Software Engineering", "Data Science"],
        "Attendance": [78.5, 74.8]
    })

    # Calculate grade distribution
    def categorize_grade(grade):
        if grade >= 70:
            return '100-70%'
        elif grade >= 60:
            return '70-60%'
        elif grade >= 50:
            return '60-50%'
        else:
            return '50-40%'

    df_combined['Grade Range'] = df_combined['Grade'].apply(categorize_grade)
    grade_distribution = df_combined.groupby(['Course', 'Grade Range']).size().unstack(fill_value=0)

    # Performance comparison data
    performance_comparison = pd.DataFrame({
        "Metric": ["Assignments", "Exams"],
        "Software Engineering": [78, 85],
        "Data Science": [74, 82]
    })

    # Calculate top performing and at-risk students
    def get_top_and_at_risk(data, course):
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        top_performing = [{"Student": s[0], "Course": course, "Grade": s[1]} for s in sorted_data[:5]]
        at_risk = [{"Student": s[0], "Course": course, "Grade": s[1]} for s in sorted_data if s[1] < 60]
        return top_performing, at_risk

    top_performing_se, at_risk_se = get_top_and_at_risk(software_engineering_data, "Software Engineering")
    top_performing_ds, at_risk_ds = get_top_and_at_risk(data_science_data, "Data Science")

    # Generate report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students Overview Report"

        # Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                        top=Side(style='thin'), bottom=Side(style='thin'))

        # Write average grades
        ws.append(["Average Grades"])
        ws.append(["Course", "Average Grade"])
        for _, row in avg_grades.iterrows():
            ws.append([row['Course'], row['Grade']])

        # Write average attendance
        ws.append([])
        ws.append(["Average Attendance"])
        ws.append(["Course", "Attendance"])
        for _, row in avg_attendance.iterrows():
            ws.append([row['Course'], row['Attendance']])

        # Write grade distribution
        ws.append([])
        ws.append(["Grade Distribution"])
        ws.append(["Course"] + list(grade_distribution.columns))
        for course, row in grade_distribution.iterrows():
            ws.append([course] + list(row))

        # Write performance comparison
        ws.append([])
        ws.append(["Performance Comparison"])
        ws.append(["Metric", "Software Engineering", "Data Science"])
        for _, row in performance_comparison.iterrows():
            ws.append([row['Metric'], row['Software Engineering'], row['Data Science']])

        # Write top performing students
        ws.append([])
        ws.append(["Top Performing Students"])
        ws.append(["Student", "Course", "Grade"])
        for student in top_performing_se + top_performing_ds:
            ws.append([student['Student'], student['Course'], student['Grade']])

        # Write at-risk students
        ws.append([])
        ws.append(["At-Risk Students"])
        ws.append(["Student", "Course", "Grade"])
        for student in at_risk_se + at_risk_ds:
            ws.append([student['Student'], student['Course'], student['Grade']])

        # Apply styling
        for row in ws[1:ws.max_row]:
            for cell in row:
                cell.border = border

        for row in ws[1:ws.max_row:len(avg_grades)+1]:
            for cell in row:
                cell.fill = header_fill

        # Prepare the Excel file for download
        with BytesIO() as b:
            wb.save(b)
            return b.getvalue()

    # Generate CSV Report
    elif file_type == "csv":
        with BytesIO() as b:
            b.write(b"Students Overview Report\n\n")
            
            b.write(b"Average Grades\n")
            avg_grades.to_csv(b, index=False)
            b.write(b"\n")
            
            b.write(b"Average Attendance\n")
            avg_attendance.to_csv(b, index=False)
            b.write(b"\n")
            
            b.write(b"Grade Distribution\n")
            grade_distribution.to_csv(b)
            b.write(b"\n")
            
            b.write(b"Performance Comparison\n")
            performance_comparison.to_csv(b, index=False)
            b.write(b"\n")
            
            b.write(b"Top Performing Students\n")
            pd.DataFrame(top_performing_se + top_performing_ds).to_csv(b, index=False)
            b.write(b"\n")
            
            b.write(b"At-Risk Students\n")
            pd.DataFrame(at_risk_se + at_risk_ds).to_csv(b, index=False)
            
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


# Export Student Attendance Insights Report (Renamed to avoid conflict)
def generate_student_attendance_insights_report(file_type="excel"):
    file_path = f"student_attendance_insights.{file_type}"

    # 📌 Sample Data (Replace with actual data retrieval from your dashboard)
    se_students = [
        ("SE6352", "Alice Johnson", 95), ("SE8934", "Bob Smith", 91), ("SE6281", "Charlie Davis", 98),
        ("SE7925", "David Martinez", 84), ("SE6726", "Eve Brown", 64), ("SE1122", "Frank Wilson", 76),
        ("SE9571", "Grace Taylor", 65), ("SE3929", "Hank Anderson", 83), ("SE7971", "Ivy Thomas", 84),
        ("SE5495", "Jack White", 78), ("SE8563", "Karen Harris", 80), ("SE3882", "Leo Martin", 73),
        ("SE4819", "Mona Clark", 99), ("SE9943", "Nathan Lewis", 71), ("SE3065", "Olivia Hall", 92),
        ("SE8912", "Peter Allen", 57), ("SE9568", "Quincy Young", 90), ("SE7547", "Rachel King", 100),
        ("SE3979", "Steve Wright", 92), ("SE5835", "Tina Scott", 63), ("SE8744", "Uma Green", 85),
        ("SE7255", "Victor Adams", 83), ("SE5697", "Wendy Baker", 92), ("SE4181", "Xander Nelson", 93),
        ("SE4762", "Yvonne Carter", 87), ("SE5070", "Zachary Mitchell", 81), ("SE8734", "Aaron Perez", 97),
        ("SE2053", "Bella Roberts", 92), ("SE8111", "Cody Gonzalez", 89), ("SE9150", "Diana Campbell", 80),
        ("SE3215", "Ethan Rodriguez", 50), ("SE5869", "Fiona Moore", 54), ("SE6168", "George Edwards", 87),
        ("SE8238", "Holly Flores", 71), ("SE3932", "Ian Cooper", 92), ("SE7659", "Julia Murphy", 89),
        ("SE4522", "Kevin Reed", 99), ("SE9236", "Laura Cox", 78), ("SE1428", "Mike Ward", 99),
        ("SE8043", "Nina Peterson", 79), ("SE7543", "Oscar Gray", 96), ("SE3569", "Paula Jenkins", 99),
        ("SE3900", "Quinn Russell", 75), ("SE8183", "Randy Torres", 94), ("SE3509", "Samantha Stevens", 65),
        ("SE1763", "Tommy Parker", 82), ("SE9793", "Ursula Evans", 85), ("SE5731", "Vince Morgan", 82),
        ("SE9781", "Whitney Bell", 81), ("SE2024", "Xavier Phillips", 75)
    ]

    ds_students = [
        ("DS1012", "Alex Carter", 71), ("DS4772", "Bella Sanders", 30), ("DS5732", "Cameron Hughes", 72),
        ("DS7477", "Diana Wright", 97), ("DS7861", "Ethan Parker", 61), ("DS9221", "Felicity James", 57),
        ("DS7221", "Gabriel Lewis", 91), ("DS6154", "Hannah Stone", 62), ("DS1486", "Ian Turner", 82),
        ("DS3966", "Jasmine Collins", 58), ("DS1166", "Kevin Morris", 90), ("DS6217", "Lara Watson", 84),
        ("DS6534", "Michael Griffin", 96), ("DS7280", "Natalie Cooper", 81), ("DS1929", "Owen Richardson", 66),
        ("DS8704", "Paige Scott", 68), ("DS5134", "Quentin Ramirez", 62), ("DS6980", "Rebecca Bennett", 92),
        ("DS3986", "Stephen Howard", 57), ("DS7376", "Tracy Bell", 82), ("DS6091", "Ulysses Barnes", 96),
        ("DS4026", "Victoria Foster", 94), ("DS4819", "Walter Henderson", 75), ("DS9065", "Xander Nelson", 84),
        ("DS9746", "Yvette Campbell", 57), ("DS3253", "Zane Mitchell", 58), ("DS6503", "Amelia Ross", 60),
        ("DS2850", "Benjamin Ward", 61), ("DS4513", "Chloe Edwards", 94), ("DS5015", "David Fisher", 59),
        ("DS3479", "Emma Butler", 60), ("DS7297", "Frederick Murphy", 57), ("DS7372", "Grace Price", 80),
        ("DS9041", "Henry Stewart", 93), ("DS6180", "Isabella Torres", 68), ("DS7380", "Jackie Peterson", 81),
        ("DS2398", "Kurt Bailey", 97), ("DS6589", "Lucy Jenkins", 84), ("DS2762", "Mason Cooper", 100),
        ("DS5804", "Nina Adams", 90), ("DS5362", "Oscar Flores", 83), ("DS5197", "Penelope Russell", 70),
        ("DS4441", "Ryan Powell", 71), ("DS8748", "Sophia Simmons", 72), ("DS8533", "Theodore White", 79),
        ("DS7065", "Ursula Martin", 73), ("DS3499", "Vince Brown", 71), ("DS5325", "William Gonzales", 85),
        ("DS7707", "Xenia Moore", 88), ("DS3801", "Zoe Walker", 73)
    ]

    # Combine SE and DS students
    all_students = se_students + ds_students

    # Create a DataFrame
    df = pd.DataFrame(all_students, columns=['Student ID', 'Student Name', 'Attendance %'])

    # ✅ Generate Excel Report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Student Attendance Insights"

        # ✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                        top=Side(style='thin'), bottom=Side(style='thin'))

        ws.append(df.columns.tolist())

        # ✅ Apply styling to headers
        for col_num, column_title in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_num, value=column_title)
            cell.fill = header_fill
            cell.border = border

        # Insert data
        for row in df.itertuples(index=False):
            ws.append(list(row))

        # ✅ Save Excel File
        wb.save(file_path)
        return file_path

    # ✅ Generate CSV Report
    elif file_type == "csv":
        df.to_csv(file_path, index=False)
        return file_path

    return None  # ✅ If invalid file_type is provided


@app.route('/download_excel_student_attendance_insights_renamed')  # 📌 Changed route name
@login_required
def download_excel_student_attendance_insights_renamed():  # 📌 Changed function name
    file_path = generate_student_attendance_insights_report("xlsx")
    return send_file(file_path, as_attachment=True, download_name="Student_Attendance_Insights.xlsx")


@app.route('/download_csv_student_attendance_insights_renamed')  # 📌 Changed route name
@login_required
def download_csv_student_attendance_insights_renamed():  # 📌 Changed function name
    file_path = generate_student_attendance_insights_report("csv")
    return send_file(file_path, as_attachment=True, download_name="Student_Attendance_Insights.csv")



#✅ Function to generate Course Registers Export
def generate_course_registers_report(file_type="excel"):
    file_path = f"course_registers.{file_type}"

    # Replace this sample data with your actual data retrieval logic
    data_science_data = [
        {"UNI ID": "DS1012", "NAME": "Alex Carter", "Role": "Student"},
        {"UNI ID": "DS4772", "NAME": "Bella Sanders", "Role": "Student"},
    ]  # Add more sample data

    software_data = [
        {"UNI ID": "SE6352", "NAME": "Alice Johnson", "Role": "Student"},
        {"UNI ID": "SE8934", "NAME": "Bob Smith", "Role": "Student"},
    ]  # Add more sample data

    # Combine SE and DS students
    all_students = data_science_data + software_data

    # Create a DataFrame
    df = pd.DataFrame(all_students, columns=['UNI ID', 'NAME', 'Role'])

    #✅ Generate Excel Report
    if file_type == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Course Registers"

        #✅ Styling
        header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
        border = Border(left=Side(style='thin'), right=Side(style='thin'),
                        top=Side(style='thin'), bottom=Side(style='thin'))

        ws.append(df.columns.tolist())

        #✅ Apply styling to headers
        for col_num, column_title in enumerate(df.columns, start=1):
            cell = ws.cell(row=1, column=col_num, value=column_title)
            cell.fill = header_fill
            cell.border = border

        # Insert data
        for row in df.itertuples(index=False):
            ws.append(list(row))
            
        # Prepare the Excel file for download
        with BytesIO() as b:
            wb.save(b)
            return b.getvalue()

    #✅ Generate CSV Report
    elif file_type == "csv":
        csv_data = df.to_csv(index=False)
        return csv_data.encode('utf-8')

    return None  #✅ If invalid file_type is provided

@app.route('/download_excel_course_registers')
@login_required
def download_excel_course_registers():
    excel_data = generate_course_registers_report("xlsx")
    return send_file(
        BytesIO(excel_data),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Course_Registers.xlsx'
    )

@app.route('/download_csv_course_registers')
@login_required
def download_csv_course_registers():
    csv_data = generate_course_registers_report("csv")
    return send_file(
        BytesIO(csv_data),
        mimetype='text/csv',
        as_attachment=True,
        download_name='Course_Registers.csv'
    )

## for admin course management


# ✅ Database Connection Function
def get_db_connection():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Initialize Courses DB (optional safety)
def init_courses_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            students INTEGER DEFAULT 0,
            lecturers INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Active',
            attendance INTEGER DEFAULT 0,
            average_grade INTEGER DEFAULT 0,
            satisfaction REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_courses_db()

# ✅ Route: Course Management Page
@app.route('/course_management')
def course_management():
    return render_template('course_management.html')

# ✅ API: Fetch All Courses for Table
@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return jsonify([dict(course) for course in courses])

# ✅ Route: View Course Page
@app.route('/course/<int:course_id>/view')
def view_course(course_id):
    conn = get_db_connection()
    course = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    conn.close()

    if course:
        return render_template('view_generic.html', course=dict(course))
    return "Course Not Found", 404

# ✅ Route: Edit Course Page (GET & POST)
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

        return redirect(url_for('course_management'))

    # GET method: show form
    course = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    conn.close()

    if course:
        return render_template('edit_generic.html', course=dict(course))
    return "Course Not Found", 404

# ✅ Delete Course
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})




    
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
