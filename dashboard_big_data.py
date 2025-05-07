# dashboard_big_data.py
from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# ✅ Use student list from course_data
from course_data import big_data_students

big_data_dashboard = Blueprint("big_data_dashboard", __name__)

def init_dashboard(flask_app):
    dash_app = dash.Dash(
        name="big_data_dashboard",
        server=flask_app,
        url_base_pathname="/dashboard_big_data/",
        suppress_callback_exceptions=True
    )

    df = pd.DataFrame(big_data_students)

    def calculate_final_grade(score, penalty):
        try:
            grade = float(score or 0)
            if penalty:
                if "Lateness Penalty" in penalty:
                    grade *= 0.95
                if "Word Count Penalty" in penalty:
                    grade *= 0.9
            return round(grade, 2)
        except:
            return 0

    df["Student"] = df["name"]
    df["ID"] = df["id"]
    df["Final Grade"] = df.apply(lambda row: calculate_final_grade(row["a1_score"], row["a1_penalty"]), axis=1)
    df["Attendance (%)"] = pd.to_numeric(df["attendance"], errors="coerce")
    df["Assignment 1 (Data Lakes)"] = pd.to_numeric(df["a1_score"], errors="coerce")
    df["Assignment 1 Status"] = df["a1_status"]
    df["Assignment 1 Penalty"] = df["a1_penalty"]
    df["Status"] = df["status"]

    df["StudentLabel"] = df["Student"]
    dupes = df["StudentLabel"].duplicated(keep=False)
    df.loc[dupes, "StudentLabel"] = df.loc[dupes].apply(
        lambda row: f"{row['Student']} ({row.get('ID', '')[-3:]})", axis=1
    )

    column_order = [
        "ID", "Student", "Final Grade", "Attendance (%)",
        "Assignment 1 (Data Lakes)", "Assignment 1 Status", "Assignment 1 Penalty", "Status"
    ]
    df = df[column_order + ["StudentLabel"]]

    dash_app.layout = html.Div(children=[
        html.H1("📊 Big Data Analytics Dashboard (DS102)", style={"textAlign": "center"}),

        dcc.Graph(id="grades-bar"),
        dcc.Graph(id="attendance-pie"),

        html.H3("📈 Insights"),
        html.P(id="avg-grade", style={"color": "#2c3e50"}),
        html.P(id="max-grade", style={"color": "#27ae60"}),
        html.P(id="min-grade", style={"color": "#c0392b"}),

        html.Label("Select Assignment:"),
        dcc.Dropdown(
            id="assignment-dropdown",
            options=[{"label": "Assignment 1 (Data Lakes)", "value": "Assignment 1 (Data Lakes)"}],
            value="Assignment 1 (Data Lakes)",
            clearable=False
        ),

        dcc.Graph(id="assignment-chart"),

        html.H2("📜 Student Performance Table", style={"textAlign": "center", "margin-top": "30px"}),

        dash_table.DataTable(
            id="data-table",
            columns=[{"name": i, "id": i} for i in column_order],
            data=df[column_order].to_dict("records"),
            sort_action="native",
            style_table={"margin": "auto", "width": "95%"},
            style_cell={"textAlign": "center"},
            style_header={"backgroundColor": "#2980b9", "color": "white"}
        ),

        dcc.Store(id='live-data', data=df.to_dict('records'))
    ])

    @dash_app.callback(
        [Output("grades-bar", "figure"),
         Output("attendance-pie", "figure"),
         Output("avg-grade", "children"),
         Output("max-grade", "children"),
         Output("min-grade", "children")],
        Input("live-data", "data")
    )
    def update_figures(data):
        df_live = pd.DataFrame(data)
        df_live["Final Grade"] = pd.to_numeric(df_live["Final Grade"], errors="coerce")
        df_live["Attendance (%)"] = pd.to_numeric(df_live["Attendance (%)"], errors="coerce")

        fig_grades = px.bar(df_live, x="StudentLabel", y="Final Grade", title="📊 Student Grades",
                            labels={"Final Grade": "Grade (%)"}, color="Final Grade", color_continuous_scale="Blues")
        fig_grades.update_layout(xaxis={'categoryorder': 'total descending'})

        attendance_pie = px.pie(
            names=["90-100%", "80-90%", "70-80%", "60-70%", "<60%"],
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

        return fig_grades, attendance_pie, avg, max_, min_

    @dash_app.callback(
        Output("assignment-chart", "figure"),
        [Input("assignment-dropdown", "value"),
         Input("live-data", "data")]
    )
    def update_assignment_chart(selected_assignment, table_data):
        df_updated = pd.DataFrame(table_data)
        df_updated[selected_assignment] = pd.to_numeric(df_updated[selected_assignment], errors="coerce")

        fig = px.bar(df_updated, x="StudentLabel", y=selected_assignment,
                     title=f"📑 {selected_assignment}",
                     labels={selected_assignment: "Score (%)"},
                     color=selected_assignment,
                     color_continuous_scale="Oranges")
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        return fig

    return dash_app


# ✅ Admin Dashboard Support

def get_big_data_attendance():
    try:
        df = pd.DataFrame(big_data_students)
        df["attendance"] = pd.to_numeric(df["attendance"], errors="coerce")
        return round(df["attendance"].mean(), 2)
    except Exception:
        return 0

def get_big_data_grade():
    def calculate_final_grade(row):
        score = float(row.get("a1_score", 0) or 0)
        penalty = row.get("a1_penalty", "")
        if "Lateness Penalty" in str(penalty):
            score *= 0.95
        if "Word Count Penalty" in str(penalty):
            score *= 0.9
        return round(score, 2)

    try:
        df = pd.DataFrame(big_data_students)
        df["Final Grade"] = df.apply(calculate_final_grade, axis=1)
        return round(df["Final Grade"].mean(), 2)
    except Exception:
        return 0
