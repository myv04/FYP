import dash
from dash import dcc, html
import plotly.graph_objs as go
import sqlite3
import json

# Create Dash app
dash_webdev = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_webdev/",
    suppress_callback_exceptions=True
)

# -------- Fetch Data from DB for Web Dev (CS202) --------
def get_webdev_data():
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM student_modules WHERE module_code = 'CS202'")
    row = c.fetchone()
    conn.close()

    if row:
        module_data = {
            "attendance": row[2],
            "grade": row[3],
            "assignments": json.loads(row[4]),
            "exams": json.loads(row[5])
        }
        return module_data
    else:
        return None

data = get_webdev_data()

# Default fallbacks if DB fails
attendance = data["attendance"] if data else 80
grade = data["grade"] if data else 79
assignments = data["assignments"] if data else []
exams = data["exams"] if data else []

# ----- Pulling Web Dev specific info -----
# Get first assignment (for visual)
assignment = assignments[0] if assignments else {"name": "Responsive Design Project", "status": "Completed", "score": 82}
assignment_name = assignment["name"]
assignment_status = assignment["status"]
assignment_score = assignment.get("score", 82)

# Get first exam
exam = exams[0] if exams else {"name": "Final Web Development Exam", "status": "Completed", "score": 76}
exam_name = exam["name"]
exam_score = exam.get("score", 76)

# Weight Distribution
exam_weight = 50
assignment_weight = 50

# Weighted grade
assignment_weighted = (assignment_score / 100) * assignment_weight
exam_weighted = (exam_score / 100) * exam_weight
current_grade = assignment_weighted + exam_weighted

# Charts

# Attendance Donut
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[attendance, 100 - attendance],
        hole=0.4,
        marker=dict(colors=["#ff8d1a", "#e0e0e0"]),
        textinfo="label+percent",
    )]
)
attendance_chart.update_layout(title="Web Development - Attendance", title_x=0.5)

# Exam + Assignment Scores
exam_assignment_chart = go.Figure()
exam_assignment_chart.add_trace(go.Bar(
    x=[exam_name, assignment_name],
    y=[exam_score, assignment_score],
    marker=dict(color=["#3498db", "#2ecc71"]),
    text=[f"{exam_score}%", f"{assignment_score}%"],
    textposition="auto",
))
exam_assignment_chart.update_layout(
    title="Exam & Assignment Scores",
    title_x=0.5,
    xaxis_title="Assessments",
    yaxis_title="Score",
    yaxis=dict(range=[0, 100])
)

# Status Bar
status_chart = go.Figure()
status_chart.add_trace(go.Bar(
    x=["Web Development"],
    y=[1],
    name="Exam Completed",
    marker=dict(color="#3498db"),
    hovertext=f"{exam_name} - Weight: {exam_weight}%"
))
status_chart.add_trace(go.Bar(
    x=["Web Development"],
    y=[1],
    name="Assignment Completed",
    marker=dict(color="#2ecc71"),
    hovertext=f"{assignment_name} - Weight: {assignment_weight}%"
))
status_chart.update_layout(
    title="Exam & Assignment Status",
    barmode="stack",
    xaxis_title="Module",
    yaxis_title="Assessments",
    legend_title="Status"
)

# Layout
dash_webdev.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px'
}, children=[

    html.H2("Web Development Dashboard", style={
        'textAlign': 'center',
        'color': '#34495e',
        'marginBottom': '30px'
    }),

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

    html.Div(dcc.Graph(figure=status_chart), style={
        'backgroundColor': 'white',
        'borderRadius': '10px',
        'padding': '20px',
        'marginTop': '30px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    })
])

# Connect Dash with Flask
def init_dashboard(server):
    dash_webdev.init_app(server)
