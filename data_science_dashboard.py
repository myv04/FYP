from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# ✅ Toggle DB mode ON
USE_DB = False


from course_data import data_science_students
raw_data = data_science_students


data_science_dashboard = Blueprint("data_science_dashboard", __name__)

def init_data_science_dashboard(flask_app):
    dash_app = dash.Dash(
        name="data_science_dashboard",
        server=flask_app,
        url_base_pathname="/data_science_dashboard/",
        suppress_callback_exceptions=True
    )

    # ✅ Updated version: handles None safely
    def calculate_final_grade(a1, a2, exam, p1, p2):
        try:
            # Convert to float if value exists, else use 0
            a1 = float(a1) if a1 is not None else 0
            a2 = float(a2) if a2 is not None else 0
            exam = float(exam) if exam is not None else 0

            grade = (a1 * 0.25) + (a2 * 0.25) + (exam * 0.5)

            if p1 and isinstance(p1, str):
                if "Lateness Penalty" in p1:
                    grade *= 0.95
                if "Word Count Penalty" in p1:
                    grade *= 0.9

            if p2 and isinstance(p2, str):
                if "Lateness Penalty" in p2:
                    grade *= 0.95
                if "Word Count Penalty" in p2:
                    grade *= 0.9

            return round(grade, 2)
        except Exception as e:
            print(f"❌ Error calculating grade: {e}")
            return 0

    df = pd.DataFrame(raw_data)

    df["Student"] = df["name"]
    df["ID"] = df["id"]

    df["Final Grade"] = df.apply(lambda row: calculate_final_grade(
    float(row["a1_score"]),
    float(row["a2_score"]),
    float(row["exam_score"]),
    row["a1_penalty"],
    row["a2_penalty"]
), axis=1)

    df["Attendance (%)"] = df["attendance"]
    df["Exam Status"] = df["exam_status"]
    df["Exam Score"] = df["exam_score"]
    df["Assignment 1 (Data Analysis)"] = df["a1_score"]
    df["Assignment 1 Status"] = df["a1_status"]
    df["Assignment 1 Penalty"] = df["a1_penalty"]
    df["Assignment 2 (Machine Learning)"] = df["a2_score"]
    df["Assignment 2 Status"] = df["a2_status"]
    df["Assignment 2 Penalty"] = df["a2_penalty"]
    df["Status"] = df["status"]


    column_order = [
        "ID", "Student", "Final Grade", "Attendance (%)", "Exam Status", "Exam Score",
        "Assignment 1 (Data Analysis)", "Assignment 1 Status", "Assignment 1 Penalty",
        "Assignment 2 (Machine Learning)", "Assignment 2 Status", "Assignment 2 Penalty", "Status"
    ]

    df = df[column_order]

    dash_app.layout = html.Div(children=[
       

        dcc.Graph(id="grades-fig"),
        dcc.Graph(id="attendance-fig"),

        html.H3("📈 Insights"),
        html.P(id="avg-grade", style={"color": "#2c3e50"}),
        html.P(id="max-grade", style={"color": "#27ae60"}),
        html.P(id="min-grade", style={"color": "#c0392b"}),

        html.Label("Select Assignment:"),
        dcc.Dropdown(
            id="assignment-dropdown",
            options=[
                {"label": "Assignment 1 (Data Analysis)", "value": "Assignment 1 (Data Analysis)"},
                {"label": "Assignment 2 (Machine Learning)", "value": "Assignment 2 (Machine Learning)"}
                ],
                    value="Assignment 1 (Data Analysis)",

            clearable=False
        ),

        dcc.Graph(id="assignment-chart"),
        dcc.Graph(id="exam-fig"),

        html.H2("📜 Student Performance Table", style={"textAlign": "center", "margin-top": "30px"}),

        dash_table.DataTable(
            id="data-table",
            columns=[{"name": i, "id": i, "editable": False} for i in column_order],
            data=df.to_dict("records"),
            sort_action="native",
            style_table={"margin": "auto", "width": "95%"},
            style_cell={"textAlign": "center"},
            style_header={"backgroundColor": "#2980b9", "color": "white"}
        ),

        dcc.Store(id='initial-table-data', data=df.to_dict('records')),
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

        fig_grades = px.bar(df_live, x="Student", y="Final Grade", title="📊 Student Grades",
                            labels={"Final Grade": "Grade (%)"}, color="Final Grade", color_continuous_scale="Blues")
        fig_grades.update_layout(xaxis={'categoryorder': 'total descending'})

        exam_fig = px.bar(df_live, x="Student", y="Exam Score", title="📝 Exam Scores",
                          labels={"Exam Score": "Score (%)"}, color="Exam Score", color_continuous_scale="Reds")
        exam_fig.update_layout(xaxis={'categoryorder': 'total descending'})

        attendance_fig = px.pie(
            names=["100-90%", "90-80%", "80-70%", "70-60%", "<60%"],
            values=[
                sum(90 <= x <= 100 for x in df_live["Attendance (%)"]),
                sum(80 <= x < 90 for x in df_live["Attendance (%)"]),
                sum(70 <= x < 80 for x in df_live["Attendance (%)"]),
                sum(60 <= x < 70 for x in df_live["Attendance (%)"]),
                sum(x < 60 for x in df_live["Attendance (%)"]),
            ],
            title="📌 Attendance Breakdown",
            hole=0.4
        )

        avg = f"📊 Average Grade: {df_live['Final Grade'].mean():.2f}%"
        max_ = f"🏆 Highest Grade: {df_live['Final Grade'].max()}%"
        min_ = f"⚠️ Lowest Grade: {df_live['Final Grade'].min()}%"

        return fig_grades, exam_fig, attendance_fig, avg, max_, min_

    @dash_app.callback(
        Output("assignment-chart", "figure"),
        [Input("assignment-dropdown", "value"),
         Input("live-data", "data")]
    )
    def update_assignment_chart(selected_assignment, table_data):
        df_updated = pd.DataFrame(table_data)
        fig = px.bar(df_updated, x="Student", y=selected_assignment, title=f"📑 {selected_assignment}",
                     labels={selected_assignment: "Score (%)"}, color=selected_assignment, color_continuous_scale="Oranges")
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        return fig

    return dash_app

# ✅ Exportable attendance average for use in admin dashboard
def get_ml_attendance():
    import pandas as pd
    from course_data import data_science_students

    df = pd.DataFrame(data_science_students)
    if df.empty or "attendance" not in df.columns:
        return 0

    return round(df["attendance"].astype(float).mean(), 2)


def get_ml_grade():
    from course_data import data_science_students
    from course_data_db import calculate_final_grade_for_df  # assuming this exists and works
    import pandas as pd

    df = pd.DataFrame(data_science_students)
    if df.empty:
        return 0

    df = calculate_final_grade_for_df(df)
    return round(df["Final Grade"].mean(), 2)
