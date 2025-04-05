import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime
import random

# Connect to SQLite database
def fetch_course_data():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return courses

# Custom function to create gauge chart
def create_gauge_chart(value, title):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1], 'color': 'red'},
                {'range': [1, 2], 'color': 'orange'},
                {'range': [2, 3], 'color': 'yellow'},
                {'range': [3, 4], 'color': 'lightgreen'},
                {'range': [4, 5], 'color': 'green'}
            ],
        }
    ))

# Initialize Dash app
dash_admin = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_admin/",
    suppress_callback_exceptions=True
)

# Initial data fetching
courses_data = fetch_course_data()

# Prepare data
courses = [course['name'].replace('BSc ', '') for course in courses_data]
students = [course['students'] for course in courses_data]
lecturers = [course['lecturers'] for course in courses_data]
attendance = [course['attendance'] for course in courses_data]
average_grade = [course['average_grade'] for course in courses_data]
satisfaction = [course['satisfaction'] for course in courses_data]

# Prepare satisfaction mapping
satisfaction_map = {course: sat for course, sat in zip(courses, satisfaction)}

# Layout for Admin Dashboard
dash_admin.layout = html.Div(style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H1("Admin Dashboard: Data Science & Software Engineering", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),

    # Dashboard Statistics
    html.Div([
        html.H2("📊 Dashboard Statistics"),
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}, children=[
            html.Div(style={'backgroundColor': '#3498db', 'padding': '20px', 'borderRadius': '10px', 'color': 'white', 'flex': '1', 'margin': '0 10px', 'textAlign': 'center'}, children=[
                html.H4("Total Students"),
                html.H2(id='total-students')
            ]),
            html.Div(style={'backgroundColor': '#2ecc71', 'padding': '20px', 'borderRadius': '10px', 'color': 'white', 'flex': '1', 'margin': '0 10px', 'textAlign': 'center'}, children=[
                html.H4("Total Lecturers"),
                html.H2(id='total-lecturers')
            ]),
            html.Div(style={'backgroundColor': '#e74c3c', 'padding': '20px', 'borderRadius': '10px', 'color': 'white', 'flex': '1', 'margin': '0 10px', 'textAlign': 'center'}, children=[
                html.H4("Courses"),
                html.H2(id='total-courses')
            ]),
        ])
    ]),

    # Quick Actions
    html.Div([
        html.H2("🚀 Quick Actions"),
        html.Button("Add New Student/Lecturer", id="add-user-btn", n_clicks=0),
        html.Button("View Recent Enrollments", id="view-enrollments-btn", n_clicks=0),
        html.Button("Review Flagged Issues", id="review-issues-btn", n_clicks=0),
        html.Button("Schedule Event", id="schedule-event-btn", n_clicks=0)
    ], style={'marginBottom': '20px'}),

    # Charts & Reports
    html.Div([
        html.H2("📈 Charts & Reports"),
        dcc.Graph(id='user-count-chart'),
        dcc.Graph(id='attendance-chart'),
        dcc.Graph(id='grade-trend-chart')
    ]),

    # Student Satisfaction
    html.Div([
        html.H2("🎓 Student Satisfaction"),
        html.Div([
            html.Div([dcc.Graph(id='satisfaction-gauge-ds')], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='satisfaction-gauge-se')], style={'width': '50%', 'display': 'inline-block'})
        ])
    ], style={'marginTop': '20px'}),

    # Notifications & Logs
    html.Div([
        html.H2("🔔 Notifications & Logs"),
        html.Ul([
            html.Li("Upcoming deadline: Final project submission (2 days left)"),
            html.Li("Warning: 5 students have attendance below 75%"),
            html.Li("New user registered: John Doe (Data Science)")
        ]),
    ], style={'marginTop': '20px'}),

    # Last Updated Time
    html.Div(id='last-updated', style={'textAlign': 'right', 'marginTop': '20px', 'color': '#7f8c8d'})
])

# ✅ Callbacks

@dash_admin.callback(
    [Output('total-students', 'children'),
     Output('total-lecturers', 'children'),
     Output('total-courses', 'children'),
     Output('last-updated', 'children')],
    [Input('add-user-btn', 'n_clicks')]
)
def update_stats(_):
    courses_data = fetch_course_data()
    total_students = sum(course['students'] for course in courses_data)
    total_lecturers = sum(course['lecturers'] for course in courses_data)
    total_courses = len(courses_data)

    return (
        f"{total_students}",
        f"{total_lecturers}",
        f"{total_courses}",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

@dash_admin.callback(Output('user-count-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_user_count_chart(_):
    courses_data = fetch_course_data()
    course_names = [course['name'].replace('BSc ', '') for course in courses_data]
    students = [course['students'] for course in courses_data]
    lecturers = [course['lecturers'] for course in courses_data]

    fig = go.Figure(data=[
        go.Bar(name='Students', x=course_names, y=students),
        go.Bar(name='Lecturers', x=course_names, y=lecturers)
    ])
    fig.update_layout(
        title="User Count by Course and Role",
        xaxis_title="Course",
        yaxis_title="Number of Users",
        barmode='group',
        legend_title="User Role"
    )
    return fig

@dash_admin.callback(Output('attendance-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_attendance_chart(_):
    courses_data = fetch_course_data()
    course_names = [course['name'].replace('BSc ', '') for course in courses_data]
    present = [course['attendance'] for course in courses_data]
    absent = [100 - course['attendance'] for course in courses_data]

    fig = go.Figure(data=[
        go.Bar(name='Present', x=course_names, y=present, marker_color='blue'),
        go.Bar(name='Absent', x=course_names, y=absent, marker_color='red')
    ])
    fig.update_layout(
        title="Course Attendance Overview",
        xaxis_title="Course",
        yaxis_title="Attendance Percentage (%)",
        barmode='stack',
        yaxis=dict(range=[0, 100]),
        legend_title="Attendance Status"
    )
    return fig

@dash_admin.callback(Output('grade-trend-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_grade_trend_chart(_):
    courses_data = fetch_course_data()
    course_names = [course['name'].replace('BSc ', '') for course in courses_data]
    grade_map = {course['name'].replace('BSc ', ''): course['average_grade'] for course in courses_data}

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    traces = []
    for course in course_names:
        grades = [round(grade_map[course] + random.uniform(-5, 5), 1) for _ in months]
        traces.append(go.Scatter(x=months, y=grades, mode='lines+markers', name=course))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Average Grade Trends by Month",
        xaxis_title="Month",
        yaxis_title="Average Grade (%)",
        legend_title="Course",
        yaxis=dict(range=[40, 100])
    )
    return fig

@dash_admin.callback(Output('satisfaction-gauge-ds', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_satisfaction_gauge_ds(_):
    courses_data = fetch_course_data()
    for course in courses_data:
        if "Data Science" in course['name']:
            return create_gauge_chart(course['satisfaction'], "Data Science Satisfaction")
    return create_gauge_chart(0, "Data Science Satisfaction")

@dash_admin.callback(Output('satisfaction-gauge-se', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_satisfaction_gauge_se(_):
    courses_data = fetch_course_data()
    for course in courses_data:
        if "Software Engineering" in course['name']:
            return create_gauge_chart(course['satisfaction'], "Software Engineering Satisfaction")
    return create_gauge_chart(0, "Software Engineering Satisfaction")

# ✅ Function to integrate with Flask
def init_admin_dashboard(server):
    dash_admin.init_app(server)

if __name__ == '__main__':
    dash_admin.run_server(debug=True)
