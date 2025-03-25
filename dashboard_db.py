import dash
from dash import dcc, html, dash_table
import plotly.graph_objs as go

# Create Dash app
dash_db = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_db/",
    suppress_callback_exceptions=True
)

# Sample Data
average_attendance = 82
remaining_attendance = 100 - average_attendance

# Exam & Assignment Data
exam_name = "Final Database Exam"
assignment_1_name = "Normalization Techniques"
assignment_2_name = "SQL Query Optimization"

assignment_1_score = 88  # Realistic score
assignment_2_score = 92  # Realistic score
exam_score = None  # Exam not done yet

# Weight Distribution
assignment_1_weight = 20
assignment_2_weight = 20
exam_weight = 60

# Calculate Weighted Grade (Only for Completed)
assignment_1_weighted = (assignment_1_score / 100) * assignment_1_weight
assignment_2_weighted = (assignment_2_score / 100) * assignment_2_weight
exam_weighted = (exam_score / 100) * exam_weight if exam_score is not None else 0

current_grade = assignment_1_weighted + assignment_2_weighted + exam_weighted

# Donut Chart (Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.4,
        marker=dict(colors=["#8e44ad", "#e0e0e0"]),
        textinfo="label+percent",
    )]
)
attendance_chart.update_layout(title="Database Management - Attendance", title_x=0.5)

# Bar Chart (Exam & Assignments Scores)
exam_assignment_chart = go.Figure()
exam_assignment_chart.add_trace(go.Bar(
    x=[assignment_1_name, assignment_2_name, exam_name],
    y=[assignment_1_score, assignment_2_score, 0 if exam_score is None else exam_score],
    marker=dict(color=["#2ecc71", "#2ecc71", "#e74c3c" if exam_score is None else "#3498db"]),
    text=[f"{assignment_1_score}%", f"{assignment_2_score}%", "TBD" if exam_score is None else f"{exam_score}%"],
    textposition="auto",
))
exam_assignment_chart.update_layout(
    title="Exam & Assignment Scores",
    title_x=0.5,
    xaxis_title="Assessments",
    yaxis_title="Score",
    yaxis=dict(range=[0, 100]),
)

# Exam & Assignment Status Chart (With Hover Info for Weight)
# Exam & Assignment Status Chart (With Two Legends)
status_chart = go.Figure()

# ✅ Both assignments under one legend
status_chart.add_trace(go.Bar(
    x=["Database Management", "Database Management"],
    y=[1, 1],
    name="Assignment Completed",  # Single legend for both assignments
    marker=dict(color="#2ecc71"),
    hovertext=[f"{assignment_1_name} - Weight: {assignment_1_weight}%", 
               f"{assignment_2_name} - Weight: {assignment_2_weight}%"]
))

# ✅ Exam has its own legend
status_chart.add_trace(go.Bar(
    x=["Database Management"],
    y=[1],
    name="Exam Not Completed",
    marker=dict(color="#e74c3c"),
    hovertext=f"{exam_name} - Weight: {exam_weight}%"
))

status_chart.update_layout(
    title="Exam & Assignment Status",
    barmode="stack",
    xaxis_title="Module",
    yaxis_title="Assessments",
    legend_title="Status"
)

# Upcoming Exam Table Data
upcoming_exams = [
    {"Exam": "Final Database Exam", "Date": "TBC"}
]

# Dashboard Layout
dash_db.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px'
}, children=[

    html.H2("Database Management Dashboard", style={
        'textAlign': 'center', 
        'color': '#34495e', 
        'marginBottom': '30px'
    }),

    # First Row: Attendance & Exam/Assignment Scores
    html.Div(style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',
        'gap': '30px',
        'justifyContent': 'center',
        'alignItems': 'center'
    }, children=[
        html.Div(dcc.Graph(figure=attendance_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),
        html.Div(dcc.Graph(figure=exam_assignment_chart), style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ]),

    # Current Grade
    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'marginTop': '30px',
        'marginBottom': '30px'
    }, children=[
        html.Div(style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'textAlign': 'center',
            'width': '300px'
        }, children=[
            html.H3("Current Grade", style={'color': '#34495e'}),
            html.P(f"{current_grade:.2f}%", style={
                'fontSize': '28px',
                'fontWeight': 'bold',
                'color': '#2ecc71' if current_grade >= 50 else '#e74c3c',
                'backgroundColor': '#ecf0f1',
                'borderRadius': '10px',
                'display': 'inline-block',
                'padding': '15px 30px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
            })
        ])
    ]),

    # Exam & Assignment Status Chart
    html.Div(dcc.Graph(figure=status_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'marginTop': '30px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }),

    # Upcoming Exam Table
    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'marginTop': '30px'
    }, children=[
        html.Div(style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'width': '400px'
        }, children=[
            html.H3("Upcoming Exams", style={'color': '#34495e', 'textAlign': 'center'}),
            dash_table.DataTable(
                columns=[
                    {"name": "Exam", "id": "Exam"},
                    {"name": "Date", "id": "Date"}
                ],
                data=upcoming_exams,
                style_header={'backgroundColor': '#8e44ad', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center', 'padding': '10px'}
            )
        ])
    ])
])

# Function to integrate with Flask
def init_dashboard(server):
    dash_db.init_app(server)
