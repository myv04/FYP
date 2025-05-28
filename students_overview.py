from flask import Blueprint
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json

students_overview = Blueprint("students_overview", __name__, template_folder="templates")

def init_students_overview(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname="/students_overview_dashboard/",
        suppress_callback_exceptions=True,
        external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"]
    )

    # Load and flatten JSON
    def load_json_data(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        data = []
        for entry in raw_data:
            if isinstance(entry, list):
                data.extend(entry)
            else:
                data.append(entry)
        return data

    se_data = load_json_data("data/software_engineering.json")
    ds_data = load_json_data("data/data_science.json")


    
    software_engineering_data = [(s["Student"], s["Final Grade"]) for s in se_data]
    data_science_data = [(s["Student"], s["Final Grade"]) for s in ds_data]

    # average attendance
    def calc_avg_attendance(data):
        return round(sum(s["Attendance"] for s in data) / len(data), 2)

    # top/at-risk
    def get_top_and_at_risk(data, course):
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        top_performing = [{"Student": s[0], "Course": course, "Grade": s[1]} for s in sorted_data[:5]]
        at_risk = [{"Student": s[0], "Course": course, "Grade": s[1]} for s in sorted_data if s[1] < 60]
        return top_performing, at_risk

    top_se, risk_se = get_top_and_at_risk(software_engineering_data, "Software Engineering")
    top_ds, risk_ds = get_top_and_at_risk(data_science_data, "Data Science")

    # Average grade chart
    avg_grades = pd.DataFrame({
        "Course": ["Software Engineering", "Data Science"],
        "Grade": [
            sum(g for _, g in software_engineering_data) / len(software_engineering_data),
            sum(g for _, g in data_science_data) / len(data_science_data)
        ]
    })
    fig_avg_grade_course = px.bar(avg_grades, x="Course", y="Grade", title="📊 Average Grade per Course",
                                   color="Grade", color_continuous_scale="Blues")

    # Attendance chart
    avg_attendance = pd.DataFrame({
        "Course": ["Software Engineering", "Data Science"],
        "Attendance": [calc_avg_attendance(se_data), calc_avg_attendance(ds_data)]
    })
    fig_attendance_course = px.bar(avg_attendance, x="Course", y="Attendance", title="📌 Average Attendance per Course",
                                    color="Attendance", color_continuous_scale="Greens")

    # Grade distribution
    def categorize_grade(grade):
        if grade >= 70:
            return '100-70%'
        elif grade >= 60:
            return '70-60%'
        elif grade >= 50:
            return '60-50%'
        else:
            return '50-40%'

    grade_ranges = ['100-70%', '70-60%', '60-50%', '50-40%']
    se_distribution = [categorize_grade(grade) for _, grade in software_engineering_data]
    ds_distribution = [categorize_grade(grade) for _, grade in data_science_data]

    software_counts = [se_distribution.count(r) for r in grade_ranges]
    data_science_counts = [ds_distribution.count(r) for r in grade_ranges]

    grade_distribution = pd.DataFrame({
        "Grade Range": grade_ranges,
        "Software Engineering": software_counts,
        "Data Science": data_science_counts
    })

    fig_grade_distribution = px.bar(
        grade_distribution, x="Grade Range", y=["Software Engineering", "Data Science"],
        title="📊 Grade Distribution by Course", barmode="group"
    )

    
    performance_comparison = pd.DataFrame({
        "Metric": ["Assignments", "Exams"],
        "Software Engineering": [78, 85],
        "Data Science": [74, 82]
    })
    fig_performance_comparison = px.bar(
        performance_comparison, x="Metric", y=["Software Engineering", "Data Science"],
        title="📈 Performance Comparison (Assignments vs Exams)", barmode="group"
    )

    dash_app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px", "maxWidth": "1200px", "margin": "auto"}, children=[
        html.H1("📌 Students Overview Dashboard", style={"textAlign": "center", "color": "#2c3e50"}),
        

        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}, children=[
            dcc.Graph(figure=fig_avg_grade_course),
            dcc.Graph(figure=fig_attendance_course)
        ]),

        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginTop": "30px"}, children=[
            dcc.Graph(figure=fig_grade_distribution),
            dcc.Graph(figure=fig_performance_comparison)
        ]),

        html.Div([
            html.H3("🚨 At-Risk Students", style={"color": "#e74c3c", "textAlign": "center"}),
            dcc.Dropdown(
                id='at-risk-dropdown',
                options=[
                    {'label': 'Software Engineering', 'value': 'SE'},
                    {'label': 'Data Science', 'value': 'DS'}
                ],
                value='SE',
                style={'width': '50%', 'margin': '10px auto'}
            ),
            dash_table.DataTable(
                id='at-risk-table',
                columns=[{"name": i, "id": i} for i in ["Student", "Course", "Grade"]],
                style_table={"overflowX": "auto", "margin": "auto", "width": "80%"},
                style_header={"backgroundColor": "#e74c3c", "color": "white", "fontWeight": "bold"},
                style_cell={"textAlign": "center"}
            )
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.H3("🌟 Top Performing Students", style={"color": "#16a085", "textAlign": "center"}),
            dcc.Dropdown(
                id='top-dropdown',
                options=[
                    {'label': 'Software Engineering', 'value': 'SE'},
                    {'label': 'Data Science', 'value': 'DS'}
                ],
                value='SE',
                style={'width': '50%', 'margin': '10px auto'}
            ),
            dash_table.DataTable(
                id='top-table',
                columns=[{"name": i, "id": i} for i in ["Student", "Course", "Grade"]],
                style_table={"overflowX": "auto", "margin": "auto", "width": "80%"},
                style_header={"backgroundColor": "#16a085", "color": "white", "fontWeight": "bold"},
                style_cell={"textAlign": "center"}
            )
        ])
    ])

    # Callbacks
    @dash_app.callback(
        Output("at-risk-table", "data"),
        [Input("at-risk-dropdown", "value")]
    )
    def update_at_risk(course):
        return risk_se if course == "SE" else risk_ds

    @dash_app.callback(
        Output("top-table", "data"),
        [Input("top-dropdown", "value")]
    )
    def update_top(course):
        return top_se if course == "SE" else top_ds
