from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import copy

from course_data import software_engineering_students
raw_data = copy.deepcopy(software_engineering_students)

for student in raw_data:
    if student["a1_status"] == "Completed" and student["a1_penalty"]:
        student["a1_status"] = "Completed"
    if student["a2_status"] == "Completed" and student["a2_penalty"]:
        student["a2_status"] = "Completed"

cloud_engineering_dashboard = Blueprint("cloud_engineering_dashboard", __name__)

def init_cloud_engineering_dashboard(flask_app):
    dash_app = dash.Dash(
        name="cloud_engineering_dashboard",
        server=flask_app,
        url_base_pathname="/cloud_engineering_dashboard/",
        suppress_callback_exceptions=True
    )

    def calculate_final_grade(a1, a2, exam, p1, p2):
        try:
            a1 = float(a1) if a1 else 0
            a2 = float(a2) if a2 else 0
            exam = float(exam) if exam else 0
            grade = (a1 * 0.25) + (a2 * 0.25) + (exam * 0.5)
            if isinstance(p1, str):
                if "Lateness Penalty" in p1: grade *= 0.95
                if "Word Count Penalty" in p1: grade *= 0.9
            if isinstance(p2, str):
                if "Lateness Penalty" in p2: grade *= 0.95
                if "Word Count Penalty" in p2: grade *= 0.9
            return round(grade, 2)
        except Exception as e:
            print(f"❌ Grade error: {e}")
            return 0

    df = pd.DataFrame(raw_data)
    df["Student"] = df["name"]
    df["ID"] = df["id"]
    df["Final Grade"] = df.apply(lambda row: calculate_final_grade(
        row.get("a1_score"), row.get("a2_score"), row.get("exam_score"),
        row.get("a1_penalty"), row.get("a2_penalty")
    ), axis=1)

    df["Attendance (%)"] = df["attendance"]
    df["Exam Status"] = df["exam_status"]
    df["Exam Score"] = df["exam_score"]
    df["Assignment 1 (Cloud Architecture Design)"] = df["a1_score"]
    df["Assignment 1 Status"] = df["a1_status"]
    df["Assignment 1 Penalty"] = df["a1_penalty"]
    df["Assignment 2 (CI/CD Pipelines in the Cloud)"] = df["a2_score"]
    df["Assignment 2 Status"] = df["a2_status"]
    df["Assignment 2 Penalty"] = df["a2_penalty"]
    df["Status"] = df["status"]

    column_order = [
        "ID", "Student", "Final Grade", "Attendance (%)", "Exam Status", "Exam Score",
        "Assignment 1 (Cloud Architecture Design)", "Assignment 1 Status", "Assignment 1 Penalty",
        "Assignment 2 (CI/CD Pipelines in the Cloud)", "Assignment 2 Status", "Assignment 2 Penalty", "Status"
    ]
    df = df[column_order]

    dash_app.layout = html.Div(children=[
        html.H1("☁️ Cloud Software Eng Dashboard (SE204)", style={"textAlign": "center"}),
        dcc.Graph(id="grades-fig"),
        dcc.Graph(id="attendance-fig"),
        html.H3("📈 Insights"),
        html.P(id="avg-grade"), html.P(id="max-grade"), html.P(id="min-grade"),
        html.Label("Select Assignment:"),
        dcc.Dropdown(
            id="assignment-dropdown",
            options=[
                {"label": "Assignment 1 (Cloud Architecture Design)", "value": "Assignment 1 (Cloud Architecture Design)"},
                {"label": "Assignment 2 (CI/CD Pipelines in the Cloud)", "value": "Assignment 2 (CI/CD Pipelines in the Cloud)"}
            ],
            value="Assignment 1 (Cloud Architecture Design)", clearable=False
        ),
        dcc.Graph(id="assignment-chart"),
        dcc.Graph(id="exam-fig"),
        html.H2("📜 Student Performance Table", style={"textAlign": "center", "margin-top": "30px"}),
        dash_table.DataTable(
            id="data-table",
            columns=[{"name": i, "id": i} for i in column_order],
            data=df.to_dict("records"),
            sort_action="native",
            style_table={"margin": "auto", "width": "95%"},
            style_cell={"textAlign": "center"},
            style_header={"backgroundColor": "#2980b9", "color": "white"}
        ),
        dcc.Store(id='live-data', data=df.to_dict('records'))
    ])

    @dash_app.callback(
        [Output("grades-fig", "figure"),
         Output("exam-fig", "figure"),
         Output("attendance-fig", "figure"),
         Output("avg-grade", "children"),
         Output("max-grade", "children"),
         Output("min-grade", "children")],
        Input("live-data", "data")
    )
    def update_all_figures(data):
        df_live = pd.DataFrame(data)
        return (
            px.bar(df_live, x="Student", y="Final Grade", title="📊 Student Grades", color="Final Grade"),
            px.bar(df_live, x="Student", y="Exam Score", title="📝 Exam Scores", color="Exam Score"),
            px.pie(
                names=["100-90%", "90-80%", "80-70%", "70-60%", "<60%"],
                values=[
                    sum(90 <= x <= 100 for x in df_live["Attendance (%)"]),
                    sum(80 <= x < 90 for x in df_live["Attendance (%)"]),
                    sum(70 <= x < 80 for x in df_live["Attendance (%)"]),
                    sum(60 <= x < 70 for x in df_live["Attendance (%)"]),
                    sum(x < 60 for x in df_live["Attendance (%)"]),
                ],
                title="📌 Attendance Breakdown", hole=0.4
            ),
            f"📊 Average Grade: {df_live['Final Grade'].mean():.2f}%",
            f"🏆 Highest Grade: {df_live['Final Grade'].max()}%",
            f"⚠️ Lowest Grade: {df_live['Final Grade'].min()}%"
        )

    @dash_app.callback(
        Output("assignment-chart", "figure"),
        [Input("assignment-dropdown", "value"), Input("live-data", "data")]
    )
    def update_assignment_chart(selected_assignment, data):
        df_updated = pd.DataFrame(data)
        fig = px.bar(df_updated, x="Student", y=selected_assignment, title=f"📑 {selected_assignment}",
                     color=selected_assignment)
        return fig

    return dash_app

from course_data import software_engineering_students  

def get_cloud_engineering_attendance():
    df = pd.DataFrame(software_engineering_students)
    df["attendance"] = pd.to_numeric(df["attendance"], errors="coerce")
    return round(df["attendance"].mean(), 2)

def get_cloud_engineering_grade():
    def calc(row):
        try:
            a1 = float(row.get("a1_score", 0))
            a2 = float(row.get("a2_score", 0))
            exam = float(row.get("exam_score", 0))
            grade = (a1 * 0.25 + a2 * 0.25 + exam * 0.5)

            for penalty in [row.get("a1_penalty", ""), row.get("a2_penalty", "")]:
                if "Lateness" in penalty: grade *= 0.95
                if "Word Count" in penalty: grade *= 0.9
            return round(grade, 2)
        except:
            return 0

    df = pd.DataFrame(software_engineering_students)
    df["Final Grade"] = df.apply(calc, axis=1)
    return round(df["Final Grade"].mean(), 2)
