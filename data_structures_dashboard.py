import dash
from dash import dcc, html
import plotly.graph_objs as go
import sqlite3
import json

# Fetch data for CS201 from student_performance.db
def fetch_dsa_data():
    conn = sqlite3.connect("student_performance.db")
    c = conn.cursor()
    c.execute("SELECT attendance, grade, exams_json FROM student_modules WHERE module_code = 'CS201'")
    row = c.fetchone()
    conn.close()

    if row:
        attendance, grade, exams_json = row
        exams = json.loads(exams_json)
        exam_score = exams[0]["score"] if exams else 0
        exam_name = exams[0]["name"] if exams else "DSA Exam"
        return attendance, grade, exam_name, exam_score
    else:
        return 0, 0, "DSA Exam", 0

# Get the data
average_attendance, current_grade, exam_name, exam_score = fetch_dsa_data()
remaining_attendance = 100 - average_attendance

# Dash app
dash_dsa = dash.Dash(
    __name__,
    routes_pathname_prefix="/dashboard_dsa/",
    suppress_callback_exceptions=True
)

# Donut Chart (Attendance)
attendance_chart = go.Figure(
    data=[go.Pie(
        labels=["Attendance", "Absent"],
        values=[average_attendance, remaining_attendance],
        hole=0.4,
        marker=dict(colors=["#ff8d1a", "#e0e0e0"]),
        textinfo="label+percent",
    )]
)
attendance_chart.update_layout(title="Data Structures & Algorithms - Attendance", title_x=0.5)

# Bar Chart (Exam Scores)
exam_chart = go.Figure()
exam_chart.add_trace(go.Bar(
    x=["DSA Exam"],
    y=[exam_score],
    marker=dict(color="#2ecc71"),
    text=[f"{exam_score}%"],
    textposition="auto",
))
exam_chart.update_layout(
    title="Data Structures & Algorithms Exam",
    title_x=0.5,
    xaxis_title="Exam",
    yaxis_title="Score",
    yaxis=dict(range=[0, 100])
)

# Status Chart
status_chart = go.Figure()
status_chart.add_trace(go.Bar(
    x=["Data Structures & Algorithms"],
    y=[1],
    name="DSA Exam",
    marker=dict(color="#2ecc71"),
    hovertext=f"{exam_name} - Score: {exam_score}%"
))
status_chart.update_layout(
    title="Exam Status",
    barmode="stack",
    xaxis_title="Course",
    yaxis_title="Status",
    legend_title="Status"
)

# Layout
dash_dsa.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'padding': '30px'
}, children=[
    html.H2("Data Structures & Algorithms Dashboard", style={
        'textAlign': 'left',
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
        html.Div(dcc.Graph(figure=exam_chart), style={
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

def init_dashboard(server):
    dash_dsa.init_app(server)
