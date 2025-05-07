from flask import Blueprint
import dash
from dash import dcc, html, Input, Output
import dash_table
import pandas as pd
import plotly.express as px
import sqlite3
import random

student_profile_dashboard = Blueprint("student_profile_dashboard", __name__)

# Module and course metadata
module_meta = {
    "SE201": {"name": "Agile Development", "assignments": ["Bugs and Fixes", "Software Architecture"], "exam": "Agile Development Exam",
              "weeks": ["Sprint Planning", "Daily Standups", "Backlog Grooming", "Scrum Events", "Velocity Tracking", "Agile Metrics", "Burndown Charts", "Product Increments", "Retrospectives", "Agile Estimation", "Kanban vs Scrum", "Agile Wrap-up"]},
    "SE202": {"name": "Web Systems", "assignments": ["Web Tech"], "exam": None,
              "weeks": ["HTML Basics", "CSS Styling", "Responsive Design", "JavaScript DOM", "Forms and Validation", "Web Hosting", "REST APIs", "Frontend Frameworks", "Authentication", "Web Security", "Debugging Tools", "Deployment"]},
    "SE203": {"name": "Software Testing and QA", "assignments": ["Unit Testing Strategies", "Test Automation Frameworks"], "exam": "Software Testing Exam",
              "weeks": ["Testing Basics", "Unit Tests", "Mocks and Stubs", "Integration Testing", "System Testing", "Acceptance Testing", "Test Automation", "Bug Tracking", "Regression Testing", "Performance Testing", "Security Testing", "Test Reporting"]},
    "SE204": {"name": "Cloud-Based Software Engineering", "assignments": ["Cloud Architecture", "CI-CD Pipelines in the Cloud"], "exam": "Cloud-Based Exam",
              "weeks": ["Cloud Basics", "IaaS & PaaS", "Deployment Models", "Cloud Storage", "Load Balancing", "Auto-scaling", "Monitoring Tools", "CI/CD Pipelines", "Containers", "Security in Cloud", "Cloud Costing", "Capstone Demo"]},
    "DS101": {"name": "Machine Learning", "assignments": ["Data Analysis", "Machine Learning"], "exam": "Machine Learning Exam",
              "weeks": ["Data Cleaning", "Feature Engineering", "Model Selection", "Supervised Learning", "Unsupervised Learning", "Neural Networks", "Evaluation Metrics", "Model Deployment", "Overfitting & Underfitting", "Hyperparameter Tuning", "Bias-Variance Tradeoff", "Final Review"]},
    "DS102": {"name": "Big Data Analytics", "assignments": ["Data Lakes"], "exam": None,
              "weeks": ["Intro to Big Data", "Hadoop Ecosystem", "Spark Basics", "Data Lakes & Warehouses", "Data Ingestion", "ETL Pipelines", "MapReduce", "Stream Processing", "Data Storage", "Scalability", "Big Data Tools", "Case Study"]},
    "DS203": {"name": "Operationalizing ML", "assignments": ["Model Deployment Strategies", "Monitoring and Logging ML Systems"], "exam": "MLOps Exam",
              "weeks": ["DevOps & MLOps", "Model Deployment", "API Integration", "Continuous Delivery", "Dockerization", "Monitoring Models", "Data Drift", "Model Logging", "Scaling Inference", "Deployment Tools", "Model Governance", "Final Review"]},
    "DS204": {"name": "Ethics and Responsible Data Use", "assignments": ["Bias and Fairness Audits", "Privacy and Consent Policies"], "exam": "Data, Ethics and Governance Exam",
              "weeks": ["Data Ethics Intro", "Bias in AI", "Fairness Metrics", "Case Studies", "Consent Mechanisms", "GDPR", "Data Security", "Responsible AI", "Transparency", "Accountability", "Audit Frameworks", "Wrap-Up"]}
}

course_modules = {
    "SE101": ["SE201", "SE202", "SE203", "SE204"],
    "DS102": ["DS101", "DS102", "DS203", "DS204"]
}

def get_db_connection():
    return sqlite3.connect("courses.db")

def simulate_attendance(attendance_pct):
    full = round(attendance_pct * 12 / 100)
    values = [100] * full + [0] * (12 - full)
    random.shuffle(values)
    return values

def init_student_profile_dashboard(flask_app):
    dash_app = dash.Dash(
        name="student_profile_dashboard",
        server=flask_app,
        url_base_pathname="/student_profile_dashboard/",
        suppress_callback_exceptions=True
    )

    dash_app.layout = html.Div(
        style={"padding": "30px 50px", "backgroundColor": "#f8f9fc"},
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(id="student-info", style={"marginBottom": "40px"}),
            html.Div(id="grade-section", style={"marginBottom": "60px"}),
            html.Div(id="attendance-section")
        ]
    )

    @dash_app.callback(
        [Output("student-info", "children"),
         Output("grade-section", "children"),
         Output("attendance-section", "children")],
        Input("url", "search")
    )
    def update_dashboard(search):
        if not search or "id=" not in search:
            return "No student ID provided.", "", ""

        sid = search.split("id=")[-1]
        conn = get_db_connection()
        query = """
        SELECT s.*, c.name as course_name, c.code as course_code
        FROM students s
        JOIN enrollments e ON s.id = e.student_id
        JOIN courses c ON c.id = e.course_id
        WHERE s.id = ?
        """
        df = pd.read_sql(query, conn, params=(sid,))
        conn.close()

        if df.empty:
            return "Student not found.", "", ""
        student = df.iloc[0]

        info = html.Div([
            html.H2(f"{student['username']} ({student['id']})"),
            html.P(f"Course: {student['course_name']} ({student['course_code']})"),
            html.P(f"Email: {student['email']}")
        ], style={"textAlign": "left", "maxWidth": "95%", "margin": "0 auto"})

        grade_tables, attendance_graphs = [], []
        modules = course_modules.get(student["course_code"], [])
        penalty_count = 0

        for mod_code in modules:
            meta = module_meta[mod_code]
            rows = []

            for i, assignment in enumerate(meta["assignments"]):
                key = f"a{i+1}"
                score = student.get(f"{key}_score")
                status = student.get(f"{key}_status")
                penalty = student.get(f"{key}_penalty")
                label = f"Assignment {i+1} – {assignment}"

                if not score and not penalty:
                    status = "Not Completed"
                elif score and not status:
                    status = "Completed"

                if penalty:
                    penalty_count += 1
                    if penalty_count > 2:
                        penalty = ""
                    elif "Lateness" in penalty and "Word" in penalty:
                        penalty = "Both Penalties"
                    elif "Lateness" in penalty:
                        penalty = "Lateness Penalty"
                    elif "Word" in penalty:
                        penalty = "Word Count Penalty"

                rows.append({
                    "Type": label,
                    "Score": score or "",
                    "Penalty": penalty or "None",
                    "Status": status or "Not Completed"
                })

            if meta["exam"]:
                exam_score = student.get("exam_score")
                exam_status = student.get("exam_status")
                score = exam_score if exam_status == "Fit to Sit" else ""
                rows.append({
                    "Type": f"Exam – {meta['exam']}",
                    "Score": score,
                    "Penalty": "",
                    "Status": exam_status or "Not Completed"
                })

            a1 = float(student.get("a1_score") or 0)
            a2 = float(student.get("a2_score") or 0)
            exam = float(student.get("exam_score") or 0)
            final = round((a1 * 0.25 + a2 * 0.25 + exam * 0.5), 2) if meta["exam"] else round((a1 * 0.5 + a2 * 0.5), 2)
            rows.append({"Type": "Final Grade", "Score": final, "Penalty": "", "Status": ""})

            grade_tables.append(html.Div([
                html.H4(f"{meta['name']} – {mod_code} Performance", style={"marginTop": "40px"}),
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in ["Type", "Score", "Penalty", "Status"]],
                    data=rows,
                    style_table={"width": "100%", "overflowX": "auto", "marginBottom": "40px"},
                    style_cell={"textAlign": "center", "padding": "10px"},
                    style_header={"backgroundColor": "#007bff", "color": "white"}
                )
            ], style={"margin": "0 auto", "maxWidth": "95%"}))

            attendance_values = simulate_attendance(student["attendance"])
            fig = px.line(
                x=[f"Week {i+1} – {topic}" for i, topic in enumerate(meta["weeks"])],
                y=attendance_values,
                markers=True,
                labels={"x": "Week", "y": "Attendance (%)"},
                title=f"{meta['name']} – {mod_code} Attendance"
            )
            fig.update_layout(xaxis_tickangle=-45)

            attendance_graphs.append(html.Div([
                dcc.Graph(figure=fig)
            ], style={"margin": "0 auto 50px", "maxWidth": "95%"}))

        return info, grade_tables, attendance_graphs

    return dash_app
