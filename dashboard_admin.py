import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime

# ✅ Import attendance functions
from software_engineering_dashboard import get_agile_attendance, get_agile_grade
from data_science_dashboard import get_ml_attendance, get_ml_grade
from dashboard_web_systems import get_web_systems_attendance, get_web_systems_grade
from dashboard_big_data import get_big_data_attendance, get_big_data_grade
from dashboard_professional_practice import get_professional_practice_attendance, get_professional_practice_grade
from mlops_dashboard import get_mlops_attendance, get_mlops_grade
from data_ethics_dashboard import get_data_ethics_attendance, get_data_ethics_grade
from software_testing_dashboard import get_software_testing_attendance, get_software_testing_grade
from cloud_engineering_dashboard import get_cloud_engineering_attendance, get_cloud_engineering_grade

# ✅ Fetch real-time data
def fetch_course_data():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    courses = conn.execute('SELECT * FROM courses').fetchall()
    result = []

    for course in courses:
        course_id = course['id']
        student_count = conn.execute('''
            SELECT COUNT(*) FROM students s
            JOIN enrollments e ON s.id = e.student_id
            WHERE e.course_id = ? AND s.role = 'Student' AND s.enrollment_status != 'Removed'
        ''', (course_id,)).fetchone()[0]

        lecturer_count = conn.execute('''
            SELECT COUNT(*) FROM students s
            JOIN enrollments e ON s.id = e.student_id
            WHERE e.course_id = ? AND s.role = 'Lecturer' AND s.enrollment_status != 'Removed'
        ''', (course_id,)).fetchone()[0]

        result.append({
            'name': course['name'],
            'year': course['year'],
            'students': student_count,
            'lecturers': lecturer_count,
            'attendance': course['attendance'],
            'average_grade': course['average_grade'],
            'satisfaction': course['satisfaction']
        })

    conn.close()
    return result

# 📊 Gauge chart helper
def create_gauge_chart(value, title):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 5]},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 1], 'color': 'red'},
                {'range': [1, 2], 'color': 'orange'},
                {'range': [2, 3], 'color': 'yellow'},
                {'range': [3, 4], 'color': 'lightgreen'},
                {'range': [4, 5], 'color': 'green'}
            ]
        }
    ))

# 🔧 Dash app setup
dash_admin = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_admin/",
    suppress_callback_exceptions=True
)

dash_admin.layout = html.Div(style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'}, children=[
    html.H1("Admin Dashboard: Data Science & Software Engineering", style={'textAlign': 'center'}),

    html.Div([
        html.H2("📊 Dashboard Statistics"),
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between'}, children=[
            html.Div(style={'backgroundColor': '#3498db', 'padding': '20px', 'color': 'white', 'flex': 1, 'margin': '0 10px'}, children=[
                html.H4("Total Students"), html.H2(id='total-students')
            ]),
            html.Div(style={'backgroundColor': '#2ecc71', 'padding': '20px', 'color': 'white', 'flex': 1, 'margin': '0 10px'}, children=[
                html.H4("Total Lecturers"), html.H2(id='total-lecturers')
            ]),
            html.Div(style={'backgroundColor': '#e74c3c', 'padding': '20px', 'color': 'white', 'flex': 1, 'margin': '0 10px'}, children=[
                html.H4("Courses"), html.H2(id='total-courses')
            ]),
        ])
    ]),

    html.Div([
        html.H2("🚀 Quick Actions"),
        html.Button("Add New Student/Lecturer", id="add-user-btn", n_clicks=0),
        html.Button("View Recent Enrollments", id="view-enrollments-btn", n_clicks=0),
        html.Button("Review Flagged Issues", id="review-issues-btn", n_clicks=0),
        html.Button("Schedule Event", id="schedule-event-btn", n_clicks=0)
    ], style={'marginTop': '20px'}),

    html.Div([
        html.H2("📈 Charts & Reports"),
        dcc.Graph(id='user-count-chart'),
        dcc.Graph(id='attendance-chart'),
        dcc.Graph(id='grade-bar-chart')
    ]),

    html.Div([
        html.H2("🎓 Student Satisfaction"),
        html.Div([
            html.Div([dcc.Graph(id='satisfaction-gauge-ds')], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='satisfaction-gauge-se')], style={'width': '50%', 'display': 'inline-block'})
        ])
    ]),

    html.Div([
        html.H2("🔔 Notifications & Logs"),
        html.Ul([
            html.Li("Upcoming deadline: Final project submission (2 days left)"),
            html.Li("Warning: 5 students have attendance below 75%"),
            html.Li("New user registered: John Doe (Data Science)")
        ])
    ], style={'marginTop': '20px'}),

    html.Div(id='last-updated', style={'textAlign': 'right', 'marginTop': '20px', 'color': '#7f8c8d'})
])

# 🔄 Stats + Last Updated
@dash_admin.callback(
    [Output('total-students', 'children'),
     Output('total-lecturers', 'children'),
     Output('total-courses', 'children'),
     Output('last-updated', 'children')],
    [Input('add-user-btn', 'n_clicks')]
)
def update_stats(_):
    data = fetch_course_data()
    return (
        sum(course['students'] for course in data),
        sum(course['lecturers'] for course in data),
        len(data),
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

# 📊 User Count Chart
@dash_admin.callback(Output('user-count-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_user_count_chart(_):
    data = fetch_course_data()
    labels = [f"{c['name'].replace('BSc ', '')} ({c['year']})" for c in data]
    students = [c['students'] for c in data]
    lecturers = [c['lecturers'] for c in data]

    fig = go.Figure(data=[
        go.Bar(name='Students', x=labels, y=students),
        go.Bar(name='Lecturers', x=labels, y=lecturers)
    ])
    fig.update_layout(
        title="User Count by Course and Year",
        xaxis_title="Course (Year)",
        yaxis_title="Number of Users",
        barmode='group',
        legend_title="User Role"
    )
    return fig

# 📉 Attendance Chart
@dash_admin.callback(Output('attendance-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_attendance_chart(_):
    modules = [
        ("DS201 - Agile Development", get_agile_attendance()),
        ("DS101 - Machine Learning", get_ml_attendance()),
        ("SE202 - Web Systems", get_web_systems_attendance()),
        ("DS102 - Big Data", get_big_data_attendance()),
        ("DSSEP1 - Professional Practice", get_professional_practice_attendance()),
        ("DS301 - MLOps", get_mlops_attendance()),
        ("DS302 - Data Ethics", get_data_ethics_attendance()),
        ("SE303 - Software Testing", get_software_testing_attendance()),
        ("SE204 - Cloud Engineering", get_cloud_engineering_attendance())
    ]
    labels = [f"{code.split(' - ')[0]}<br><b>{code.split(' - ')[1]}</b>" for code, _ in modules]
    attendance = [score for _, score in modules]
    absent = [100 - score for score in attendance]

    fig = go.Figure([
        go.Bar(name="Present (%)", x=labels, y=attendance, marker_color="green"),
        go.Bar(name="Absent (%)", x=labels, y=absent, marker_color="red")
    ])
    fig.update_layout(
        barmode="stack",
        title="🧮 Average Attendance by Module (2025)",
        yaxis=dict(title="Attendance %", range=[0, 100]),
        xaxis=dict(title="Module", tickangle=0),
        legend_title="Status"
    )
    return fig

# 📈 Grade Chart
@dash_admin.callback(Output('grade-bar-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_grade_chart(_):
    modules = [
        ("DS201 - Agile Development", get_agile_grade()),
        ("DS101 - Machine Learning", get_ml_grade()),
        ("SE202 - Web Systems", get_web_systems_grade()),
        ("DS102 - Big Data", get_big_data_grade()),
        ("DSSEP1 - Professional Practice", get_professional_practice_grade()),
        ("DS301 - MLOps", get_mlops_grade()),
        ("DS302 - Data Ethics", get_data_ethics_grade()),
        ("SE303 - Software Testing", get_software_testing_grade()),
        ("SE204 - Cloud Engineering", get_cloud_engineering_grade())
    ]
    labels = [f"{code.split(' - ')[0]}<br><b>{code.split(' - ')[1]}</b>" for code, _ in modules]
    values = [grade for _, grade in modules]

    fig = go.Figure([
        go.Bar(name="Average Grade (%)", x=labels, y=values, marker_color="mediumpurple")
    ])
    fig.update_layout(
        title="📉 Average Grade by Module (2025)",
        yaxis=dict(title="Grade %", range=[0, 100]),
        xaxis=dict(title="Module")
    )
    return fig

# 🎓 Satisfaction Gauges
@dash_admin.callback(Output('satisfaction-gauge-ds', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_satisfaction_gauge_ds(_):
    for course in fetch_course_data():
        if "Data Science" in course['name']:
            return create_gauge_chart(course['satisfaction'], "Data Science Satisfaction")
    return create_gauge_chart(0, "Data Science Satisfaction")

@dash_admin.callback(Output('satisfaction-gauge-se', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_satisfaction_gauge_se(_):
    for course in fetch_course_data():
        if "Software Engineering" in course['name']:
            return create_gauge_chart(course['satisfaction'], "Software Engineering Satisfaction")
    return create_gauge_chart(0, "Software Engineering Satisfaction")

# 🔌 Integrate with Flask
def init_admin_dashboard(server):
    dash_admin.init_app(server)

if __name__ == '__main__':
    dash_admin.run_server(debug=True)
