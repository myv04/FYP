import random
import json
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
from flask import Blueprint
import os

student_attendance_insights = Blueprint("student_attendance_insights", __name__, template_folder="templates")

attendance_cache = {}

def init_student_attendance_insights(flask_app):
    dash_app = dash.Dash(
        name="student_attendance_insights",
        server=flask_app,
        url_base_pathname="/student_attendance_insights/",
        suppress_callback_exceptions=True
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    def load_json_data(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        flat = []
        for entry in data:
            if isinstance(entry, list):
                flat.extend(entry)
            else:
                flat.append(entry)
        return [(s["ID"], s["Student"], s["Attendance"]) for s in flat]

    se_students = load_json_data(os.path.join(DATA_DIR, "software_engineering.json"))
    ds_students = load_json_data(os.path.join(DATA_DIR, "data_science.json"))

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
    se_week_labels = [f"Week {i+1} ({se_lectures[i]})" for i in range(12)]
    ds_week_labels = [f"Week {i+1} ({ds_lectures[i]})" for i in range(12)]

    def create_student_graphs(students, week_labels):
        student_graphs = {}
        total_weeks = len(week_labels)

        for student_id, student_name, attendance in students:
            cache_key = student_id
            if cache_key in attendance_cache:
                week_attendance = attendance_cache[cache_key]
            else:
                attended_weeks_count = round((attendance / 100) * total_weeks)
                attended_indices = sorted(random.sample(range(total_weeks), attended_weeks_count))
                week_attendance = [100 if i in attended_indices else 0 for i in range(total_weeks)]
                attendance_cache[cache_key] = week_attendance

            student_data = [{"Week": week_labels[i], "Attendance %": week_attendance[i]} for i in range(total_weeks)]
            student_df = pd.DataFrame(student_data)

            fig = px.line(student_df, x="Week", y="Attendance %",
                          title=f"{student_id} - {student_name}'s Attendance",
                          markers=True)

            fig.update_traces(
                mode="lines+markers",
                line=dict(color="#0055ff", width=3),
                marker=dict(size=10, color="#ffffff", line=dict(width=2, color="#0055ff"))
            )

            fig.update_layout(
                autosize=True,
                height=450,
                yaxis=dict(range=[-5, 105], tickvals=[0, 50, 100], gridcolor="lightgrey"),
                xaxis=dict(tickangle=-45, gridcolor="lightgrey"),
                hovermode="x unified",
                font=dict(size=14),
                margin=dict(l=40, r=40, t=50, b=60),
                paper_bgcolor="#f9f9f9",
                plot_bgcolor="#ffffff"
            )

            student_graphs[f"{student_id} - {student_name}"] = dcc.Graph(
                figure=fig,
                style={
                    'width': '100%',
                    'padding': '20px',
                    'borderRadius': '16px',
                    'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.08)',
                    'backgroundColor': '#fff'
                }
            )

        return student_graphs

    se_graphs = create_student_graphs(se_students, se_week_labels)
    ds_graphs = create_student_graphs(ds_students, ds_week_labels)

    dash_app.layout = html.Div([
        html.H1("📊 Student Attendance Insights", style={"textAlign": "center", "marginBottom": "20px"}),

        html.Div([
            dcc.Dropdown(
                id='course-dropdown',
                options=[
                    {'label': 'Software Engineering', 'value': 'SE'},
                    {'label': 'Data Science', 'value': 'DS'}
                ],
                value='SE',
                style={'marginBottom': '20px'}
            ),
            dcc.Dropdown(
                id='student-dropdown',
                multi=True,
                style={'marginBottom': '20px'}
            )
        ], style={
            'width': '80%',
            'margin': '0 auto',
            'padding': '20px',
            'backgroundColor': '#f4f6f8',
            'borderRadius': '16px',
            'boxShadow': '0 2px 6px rgba(0,0,0,0.05)'
        }),

        html.Div(id='graphs-container', style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fill, minmax(500px, 1fr))",
            "gap": "20px",
            "padding": "30px"
        })
    ])

    @dash_app.callback(
        Output('student-dropdown', 'options'),
        Output('student-dropdown', 'value'),
        Input('course-dropdown', 'value')
    )
    def update_student_dropdown(selected_course):
        students = se_students if selected_course == 'SE' else ds_students
        options = [{'label': f"{id} - {name}", 'value': f"{id} - {name}"} for id, name, _ in students]
        return options, []

    @dash_app.callback(
        Output('graphs-container', 'children'),
        Input('course-dropdown', 'value'),
        Input('student-dropdown', 'value')
    )
    def update_graphs(course, selected_students):
        graphs = se_graphs if course == 'SE' else ds_graphs
        return [graphs[s] for s in selected_students] if selected_students else list(graphs.values())

    return dash_app