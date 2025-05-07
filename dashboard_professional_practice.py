from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import sqlite3
import pandas as pd
import plotly.express as px

shared_dashboard = Blueprint("shared_dashboard", __name__)

def init_shared_module_dashboard(flask_app):
    dash_app = dash.Dash(
        name="shared_module_dashboard",
        server=flask_app,
        url_base_pathname="/admin/modules/shared-professional-practice/",
        suppress_callback_exceptions=True
    )

    def load_data():
        conn = sqlite3.connect("courses.db")
        df = pd.read_sql_query("SELECT * FROM dashboard_professional_practice", conn)
        conn.close()

        df["Student"] = df["name"]
        df["ID"] = df["id"]
        df["Assignment 1 (Ethics in Tech)"] = df["a1_score"]
        df["Assignment 2 (Team Collaboration Report)"] = df["a2_score"]
        df["Attendance (%)"] = df["attendance"]
        df["Final Grade"] = (df["a1_score"] * 0.4 + df["a2_score"] * 0.4 + df["attendance"] * 0.2).round(2)
        return df

    df = load_data()
    column_order = [
        "ID", "Student", "course", "Final Grade", "Attendance (%)",
        "Assignment 1 (Ethics in Tech)", "Assignment 2 (Team Collaboration Report)"
    ]

    df = df[column_order]

    dash_app.layout = html.Div(children=[
        html.H1("📘 Professional Practice - Shared Module", style={"textAlign": "center"}),

        html.Label("Filter by Course:"),
        dcc.Dropdown(
            id="course-filter",
            options=[
                {"label": "All", "value": "All"},
                {"label": "Data Science", "value": "Data Science"},
                {"label": "Software Engineering", "value": "Software Engineering"}
            ],
            value="All",
            clearable=False
        ),

        html.Br(),
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
                {"label": "Assignment 1 (Ethics in Tech)", "value": "Assignment 1 (Ethics in Tech)"},
                {"label": "Assignment 2 (Team Collaboration Report)", "value": "Assignment 2 (Team Collaboration Report)"}
            ],
            value="Assignment 1 (Ethics in Tech)",
            clearable=False
        ),

        dcc.Graph(id="assignment-chart"),

        html.H2("📜 Student Performance Table", style={"textAlign": "center", "margin-top": "30px"}),
        dash_table.DataTable(
            id="data-table",
            columns=[{"name": i, "id": i, "editable": False} for i in column_order],
            data=df.to_dict("records"),
            sort_action="native",
            style_table={"margin": "auto", "width": "95%"},
            style_cell={"textAlign": "center"},
            style_header={"backgroundColor": "#007BFF", "color": "white"}
        ),

        dcc.Store(id='live-data', data=df.to_dict('records'))
    ])

    @dash_app.callback(
        [Output("grades-fig", "figure"),
         Output("attendance-fig", "figure"),
         Output("avg-grade", "children"),
         Output("max-grade", "children"),
         Output("min-grade", "children"),
         Output("live-data", "data"),
         Output("data-table", "data")],
        Input("course-filter", "value")
    )
    def update_all_figures(course):
        df = load_data()
        if course != "All":
            df = df[df["course"] == course]

        fig_grades = px.bar(df, x="Student", y="Final Grade", title="📊 Student Final Grades",
                            labels={"Final Grade": "Grade (%)"}, color="Final Grade", color_continuous_scale="Blues")

        attendance_fig = px.pie(
            names=["100-90%", "90-80%", "80-70%", "<70%"],
            values=[
                sum(90 <= x <= 100 for x in df["Attendance (%)"]),
                sum(80 <= x < 90 for x in df["Attendance (%)"]),
                sum(70 <= x < 80 for x in df["Attendance (%)"]),
                sum(x < 70 for x in df["Attendance (%)"]),
            ],
            title="📌 Attendance Breakdown",
            hole=0.4
        )

        avg = f"📊 Average Final Grade: {df['Final Grade'].mean():.2f}%"
        max_ = f"🏆 Highest Grade: {df['Final Grade'].max()}%"
        min_ = f"⚠️ Lowest Grade: {df['Final Grade'].min()}%"

        return fig_grades, attendance_fig, avg, max_, min_, df.to_dict('records'), df.to_dict("records")

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

def get_professional_practice_attendance():
    import pandas as pd
    import sqlite3

    conn = sqlite3.connect("courses.db")
    df = pd.read_sql_query("SELECT * FROM dashboard_professional_practice", conn)
    conn.close()

    if df.empty or "attendance" not in df.columns:
        return 0

    return round(df["attendance"].astype(float).mean(), 2)

def get_professional_practice_grade():
    import pandas as pd
    import sqlite3

    conn = sqlite3.connect("courses.db")
    df = pd.read_sql_query("SELECT * FROM dashboard_professional_practice", conn)
    conn.close()

    if df.empty or "a1_score" not in df.columns or "a2_score" not in df.columns or "attendance" not in df.columns:
        return 0

    df["Final Grade"] = (df["a1_score"] * 0.4 + df["a2_score"] * 0.4 + df["attendance"] * 0.2)
    return round(df["Final Grade"].mean(), 2)
