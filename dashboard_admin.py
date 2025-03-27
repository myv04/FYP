import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import random

# Create Dash app
dash_admin = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_admin/",
    suppress_callback_exceptions=True
)

# Sample Data (Admin Perspective)
courses = ["Data Science", "Software Engineering"]
total_students = {"Data Science": 450, "Software Engineering": 500}
total_lecturers = {"Data Science": 25, "Software Engineering": 30}
average_attendance = {"Data Science": 82, "Software Engineering": 78}
average_grade = {"Data Science": 68, "Software Engineering": 64}  # Changed to percentages
student_satisfaction = {"Data Science": 4.2, "Software Engineering": 4.0}

# Custom function to create a gauge chart
def create_gauge_chart(value, title):
    return go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
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
            html.Div([
                dcc.Graph(id='satisfaction-gauge-ds')
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='satisfaction-gauge-se')
            ], style={'width': '50%', 'display': 'inline-block'})
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

# Callbacks
@dash_admin.callback(
    [Output('total-students', 'children'),
     Output('total-lecturers', 'children'),
     Output('total-courses', 'children'),
     Output('last-updated', 'children')],
    [Input('add-user-btn', 'n_clicks')]
)
def update_stats(_):
    return (
        f"{sum(total_students.values())}",
        f"{sum(total_lecturers.values())}",
        f"{len(courses)}",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

@dash_admin.callback(Output('user-count-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_user_count_chart(_):
    fig = go.Figure(data=[
        go.Bar(name='Students', x=courses, y=[total_students[course] for course in courses]),
        go.Bar(name='Lecturers', x=courses, y=[total_lecturers[course] for course in courses])
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
    present = [average_attendance[course] for course in courses]
    absent = [100 - average_attendance[course] for course in courses]

    fig = go.Figure(data=[
        go.Bar(name='Present', x=courses, y=present, marker_color='blue'),
        go.Bar(name='Absent', x=courses, y=absent, marker_color='red')
    ])
    fig.update_layout(
        title="Course Attendance Overview",
        xaxis_title="Course",
        yaxis_title="Attendance Percentage (%)",  # ✅ Clear label
        barmode='stack',
        yaxis=dict(range=[0, 100]),  # ✅ Corrected
        legend_title="Attendance Status"
    )
    return fig

@dash_admin.callback(Output('grade-trend-chart', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_grade_trend_chart(_):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ds_grades = [round(average_grade['Data Science'] + random.uniform(-5, 5), 1) for _ in range(12)]
    se_grades = [round(average_grade['Software Engineering'] + random.uniform(-5, 5), 1) for _ in range(12)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=ds_grades, mode='lines+markers', name='Data Science'))
    fig.add_trace(go.Scatter(x=months, y=se_grades, mode='lines+markers', name='Software Engineering'))
    
    fig.update_layout(
        title="Average Grade Trends by Month",
        xaxis_title="Month",
        yaxis_title="Average Grade (%)",
        legend_title="Course",
        yaxis=dict(range=[40, 100])  # Adjusted to show a realistic range for UK university grades
    )
    return fig

@dash_admin.callback(Output('satisfaction-gauge-ds', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_satisfaction_gauge_ds(_):
    return create_gauge_chart(student_satisfaction['Data Science'], "Data Science Satisfaction")

@dash_admin.callback(Output('satisfaction-gauge-se', 'figure'), [Input('add-user-btn', 'n_clicks')])
def update_satisfaction_gauge_se(_):
    return create_gauge_chart(student_satisfaction['Software Engineering'], "Software Engineering Satisfaction")

# Function to integrate with Flask
def init_admin_dashboard(server):
    dash_admin.init_app(server)

if __name__ == '__main__':
    dash_admin.run_server(debug=True)
