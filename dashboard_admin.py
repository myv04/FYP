import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime

#  Import attendance functions
from software_engineering_dashboard import get_agile_attendance, get_agile_grade
from data_science_dashboard import get_ml_attendance, get_ml_grade
from dashboard_web_systems import get_web_systems_attendance, get_web_systems_grade
from dashboard_big_data import get_big_data_attendance, get_big_data_grade
from dashboard_professional_practice import get_professional_practice_attendance, get_professional_practice_grade
from mlops_dashboard import get_mlops_attendance, get_mlops_grade
from data_ethics_dashboard import get_data_ethics_attendance, get_data_ethics_grade
from software_testing_dashboard import get_software_testing_attendance, get_software_testing_grade
from cloud_engineering_dashboard import get_cloud_engineering_attendance, get_cloud_engineering_grade


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


dash_admin = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_admin/",
    suppress_callback_exceptions=True
)

dash_admin.layout = html.Div(style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'}, children=[

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
        html.H2("🔔 Notifications & Logs"),
        html.Ul([
            html.Li("Upcoming deadline: Final project report (2 days left)"),
            html.Li("New user registered: DR Emily Roberts (BSc Data Science DS102)")
        ])
    ], style={
        'marginTop': '20px',
        'padding': '15px',
        'backgroundColor': '#fefefe',
        'border': '1px solid #ddd',
        'borderRadius': '8px',
        'boxShadow': '0 1px 4px rgba(0,0,0,0.1)'
    }),

    html.Div([
        html.H2("📈 Charts & Reports"),
        dcc.Graph(id='user-count-chart'),
        dcc.Graph(id='attendance-chart'),
        dcc.Graph(id='grade-bar-chart')
    ]),

    html.Div([
        html.H2("🎓 Course Overview Summary"),
        html.Table([
            html.Tr([
                html.Th("Courses Under Management", style={'fontSize': '18px', 'border': '1px solid black'}),
                html.Th("Modules", style={'fontSize': '18px', 'border': '1px solid black'})
            ]),
            html.Tr([
                html.Td("2", style={'fontSize': '36px', 'fontWeight': 'bold', 'color': 'red', 'border': '1px solid black'}),
                html.Td("9", style={'fontSize': '36px', 'fontWeight': 'bold', 'color': 'red', 'border': '1px solid black'})
            ]),
            html.Tr([
                html.Th("Shared Modules", style={'fontSize': '18px', 'border': '1px solid black'}),
                html.Th("Upcoming Reviews", style={'fontSize': '18px', 'border': '1px solid black'})
            ]),
            html.Tr([
                html.Td("1", style={'fontSize': '36px', 'fontWeight': 'bold', 'color': 'red', 'border': '1px solid black'}),
                html.Td("3", style={'fontSize': '36px', 'fontWeight': 'bold', 'color': 'red', 'border': '1px solid black'})
            ]),
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'textAlign': 'center'
        }),
    ], style={
        'marginTop': '30px',
        'padding': '20px',
        'backgroundColor': '#ecf0f1'
    }),

    html.Div(id='last-updated', style={'textAlign': 'right', 'marginTop': '20px', 'color': '#7f8c8d'})
])

# 🔄 Stats + Last Updated
@dash_admin.callback(
    [Output('total-students', 'children'),
     Output('total-lecturers', 'children'),
     Output('total-courses', 'children'),
     Output('last-updated', 'children')],
    [Input('user-count-chart', 'figure')]
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
@dash_admin.callback(Output('user-count-chart', 'figure'), [Input('total-students', 'children')])
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
@dash_admin.callback(Output('attendance-chart', 'figure'), [Input('total-students', 'children')])
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
@dash_admin.callback(Output('grade-bar-chart', 'figure'), [Input('total-students', 'children')])
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

# 🔌 Integrate with Flask
def init_admin_dashboard(server):
    dash_admin.init_app(server)

if __name__ == '__main__':
    dash_admin.run_server(debug=True)
